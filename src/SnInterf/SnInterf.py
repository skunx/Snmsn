#! /usr/bin/env python

'''
@author: Daouzli
'''


import SnGui #container for ip->account->contact

import pygtk
pygtk.require('2.0')
import gtk


class SnGtkWindow():
    """Class containing the GtkWindow and the treeview"""
    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, sn):
        self.sn = sn
        
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("SnMSN Gui")
        self.window.set_size_request(600, 200)
        self.window.connect("delete_event", self.delete_event)
        
        # create a TreeStore with one string column to use as the model
        self.explorer_tree = gtk.TreeStore(str)
        
        # create the TreeView using explorer_tree
        self.treeview = gtk.TreeView(self.explorer_tree)
        treeselection = self.treeview.get_selection()
        treeselection.set_mode(gtk.SELECTION_SINGLE)
        self.treeview.connect("row-activated", self.selection)
          
        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Explorer')
        
        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)
        
        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()
        
        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)
        
        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in explorer_tree
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        
        # make it searchable
        self.treeview.set_search_column(0)
        #scrolltreeview = gtk.VScrollbar(adjustment=None)
        #scrolltreeview.add_child(self.treeview)
        
        #create the data window
        self.data_window = gtk.Notebook()
        
        #create the text zone for the speech
        self.label_speech = gtk.Label("[No speech]")
        
        self.gui = gtk.HBox(False, 2)
        self.data_win = gtk.VBox(False, 1)
        
        self.label_select = gtk.Label("[No selection]")
        self.label_select.set_alignment(0, 0)
        
        self.data_win.pack_start(self.label_select, True, True, 0)
        self.data_win.pack_start(self.data_window, True, True, 0)
        
        #treeview is placed on the left, then its vscrollbar, and then the data window on the right
        self.tvscrv=gtk.VScrollbar(self.treeview.get_vadjustment())
        self.gui.pack_start(self.treeview, True, True, 10)
        self.gui.pack_start(self.tvscrv, True, True, 10)
        self.gui.pack_start(self.data_win, True, True, 10)
        
        #config the data window zone
        self.config_data_window()
        
        self.window.add(self.gui)

        self.window.show_all()

    def selection(self, widget, event, data=None):
        """selection(): shows the selected contact item in data window label zone, 
                        and if there is a speech, shows it on the speech zone.
                        if the selection is not a contact, it expands or collapses the child rows """
        if len(event) == 3: #work only in the 3rd level (selection of a contact)
            ip,acc,cont = event
            s = '%s->%s->%s' %  (self.sn.ip_id(ip).ip,
                                     self.sn.ip_id(ip).account_id(acc).account,
                                     self.sn.ip_id(ip).account_id(acc).contact_id(cont).contact)
            self.set_label_selected(s)

            self.set_label_speech(self.sn.ip_id(ip).account_id(acc).contact_id(cont).speech)
        else:
            if self.treeview.row_expanded(event):
                self.treeview.collapse_row(event)
            else:
                self.treeview.expand_row(event, False)
    
    def config_data_window(self):
        """config_data_window(): creates the data window zone (right part)"""
        self.data_window.set_tab_pos(2) #the tabs will be placed on the top
        label = gtk.Label("Speech")#the first tab's label is Speech
        self.data_window.append_page(self.label_speech, label)#add the speech zone to the data window notebook
        self.window.show_all()
        
    def set_label_selected(self, label):
        """set_label_speech(speech): Sets the text of the speech showed on the data window speech tab"""
        self.label_select.set_text(label)
        self.window.show_all()
        
    def set_label_speech(self, speech):
        """set_label_speech(speech): Sets the text of the speech showed on the data window speech tab"""
        self.label_speech.set_text(speech)
        self.window.show_all()
        
    def create_sn_tree(self):
        """create_sn_tree(sn): creates (after erasing old) and shows a treeview based on the Sn_Gui object content"""
        sn = self.sn
        self.explorer_tree.clear()
        for ip in sn.list_ips():
            parent_ip=self.explorer_tree.append(None, ['%s' % sn.ip(ip).ip])
            print("i" + str(parent_ip))
            for acc in sn.ip(ip).list_accounts():
                child_acc=self.explorer_tree.append(parent_ip, ['%s' % sn.ip(ip).account(acc).account])
                print("  a" + str(child_acc))
                for cont in sn.ip(ip).account(acc).list_contacts():
                    print("     " + str(self.explorer_tree.append(child_acc, ['%s' % sn.ip(ip).account(acc).contact(cont).contact])))
        self.window.show_all()
    
    def update_sn_tree(self):
        """update_sn_tree(): Searchs in Sn object if there are data not yet in the tree and update it if necessary"""
        sn = self.sn
        tr = self.explorer_tree
        for ip in sn.list_ips():
            self.add_if_not_sn_ip_tree(ip)
            for acc in sn.ip(ip).list_accounts():
                self.add_if_not_sn_account_tree(ip,acc)
                for cont in sn.ip(ip).account(acc).list_contacts():
                    self.add_if_not_sn_contact_tree(ip,acc,cont)
        
    def show(self):
        self.window.show_all()
        
    def add_if_not_sn_ip_tree(self,ip):
        """add_if_not_sn_ip_tree(ip): add the ip to the tree if doesn't exists and return the iter"""
        tr=self.explorer_tree
        nb=tr.iter_n_children(None)
        is_ip=False
        for i in range(nb):
            ipiter=tr.iter_nth_child(None,i)
            if tr.get_value(ipiter,0)==ip:
                is_ip=True
                break
        if is_ip==False:
            ipiter=self.explorer_tree.append(None, ['%s' % ip])
        return ipiter
            
    def add_if_not_sn_account_tree(self, ip, acc):
        """add_if_not_sn_account_tree(ip,acc): add the ip->acc to the tree if doesn't exists and return the iter"""
        ipiter = self.add_if_not_sn_ip_tree(ip)
        tr = self.explorer_tree
        is_acc = False
        nb = tr.iter_n_children(ipiter)
        for i in range(nb):
            acciter = tr.iter_nth_child(ipiter, i)
            if tr.get_value(acciter, 0) == acc:
                is_acc = True 
                break  
        if is_acc == False:
            acciter = self.explorer_tree.append(ipiter, ['%s' % acc])
        return acciter

    def add_if_not_sn_contact_tree(self, ip, acc, cont):
        """add_if_not_sn_contact_tree(ip,acc,cont): add the ip->acc->cont to the tree if doesn't exists and return the iter"""
        acciter = self.add_if_not_sn_account_tree(ip, acc)
        tr = self.explorer_tree
        is_cont = False
        nb = tr.iter_n_children(acciter)
        for i in range(nb):
            contiter = tr.iter_nth_child(acciter, i)
            if tr.get_value(contiter, 0) == cont:
                is_cont = True 
                break  
        if is_cont == False:
            contiter = self.explorer_tree.append(acciter, ['%s' % cont])
        return contiter

if __name__ == "__main__":

    def main():
        gtk.main()

    g=SnGui.SnGui()
    tvSn=SnGtkWindow(g)

    g.add_ip("192.168.0.10")
    g.ip("192.168.0.10").add_account("popo@hotmail.com")
    g.ip("192.168.0.10").add_account("didi@hotmail.com")
    g.ip("192.168.0.10").account("didi@hotmail.com").add_contact("coco")
    g.ip("192.168.0.10").account("popo@hotmail.com").add_contact("coco")
    g.ip("192.168.0.10").account("popo@hotmail.com").contact("coco").new_speech("je suis le coco de popo")
    g.ip("192.168.0.10").account("popo@hotmail.com").add_contact("titi")

    g.add_ip("192.168.0.3")
    g.ip("192.168.0.3").add_account("piouf@hotmail.com")
    g.ip("192.168.0.3").add_account("raaaa@hotmail.com")
    g.ip("192.168.0.3").account("piouf@hotmail.com").add_contact("nun")
    g.ip("192.168.0.3").account("piouf@hotmail.com").contact("nun").new_speech("moi le nun de piouf")
    g.ip("192.168.0.3").account("piouf@hotmail.com").contact("nun").add_to_speech("\nah bon!\noui oui tout a fit!\n\nhihi hoho que c'est trop rigolo poils au dos")
    

    g.add_ip("192.168.0.1")
    tvSn.create_sn_tree()
    tvSn.add_if_not_sn_account_tree("192.168.0.11","luf@hotmail.ci")
    g.add_ip("192.168.0.11")
    g.ip("192.168.0.11").add_account("luf@hotmail.ci")
    g.ip("192.168.0.11").account("luf@hotmail.ci").add_contact("lulu")
    tvSn.add_if_not_sn_account_tree("192.168.0.10","luf@hotmail.ci")
    tvSn.update_sn_tree()
    tvSn.show()
    #tvSn.set_label_speech(g.ip("192.168.0.3").account("piouf@hotmail.com").contact("nun").speech)
    #tvSn.set_label_selected("192.168.0.3->piouf@hotmail.com->nun")
    main()

