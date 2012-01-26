#! /usr/bin/env python
'''
@author: Daouzli
'''
from SnGui import SnGui      #container for ip->account->contact
from SnInterf import SnInterf   #gtk window with the treeview
from SnProtocol import SnProtocol #filtering packets with msn protocol

import re
import sys
import pcap
import string
import time
import socket
import struct
import gobject

global g    #class SnGui 
global tvSn #class SnInterf
global prot #class SnProtocol
    
protocols={socket.IPPROTO_TCP:'tcp',
            socket.IPPROTO_UDP:'udp',
            socket.IPPROTO_ICMP:'icmp'}

def decode_ip_packet(s):
    d={}
    d['version']=(ord(s[0]) & 0xf0) >> 4
    d['header_len']=ord(s[0]) & 0x0f
    d['tos']=ord(s[1])
    d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
    d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
    d['flags']=(ord(s[6]) & 0xe0) >> 5
    d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
    d['ttl']=ord(s[8])
    d['protocol']=ord(s[9])
    d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
    d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
    d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
    if d['header_len']>5:
        d['options']=s[20:4*(d['header_len']-5)]
    else:
        d['options']=None
    d['data']=s[4*d['header_len']:]
    return d
ips={}


def det_IP_packet(addr):
    """det_IP_packet(addr): add the IP addr to the stored data and add it to the treeview"""
    global g,tvSn
    global ips
    if addr not in ips.keys():
        ips[addr]={}
        g.add_ip(addr)
        #tvSn.create_sn_tree()
        #tvSn.update_sn_tree()
        tvSn.add_if_not_sn_ip_tree(addr)
   
def det_elems_data(data,src,dst):
    """det_elems_data(data,src,dst): analyse the data from packet sent from src IP to dst IP"""
    global g,prot,tvSn
    print len(data)
    cmd=re.findall(r'^(\w+)\s',data)
    if len(cmd)>0:
        for i in cmd:
            print "COMMAND : "+i

    prot.set_data(data)
    if prot.is_email()==True: #if the data contains an email
        mail=prot.get_email()
        for i in mail:
            print i+" from "+src+" to "+dst
    adrip=dst if src[:6]=='207.46' or src[:4]=='65.5' else src #if M$ server then use the other ip adress
    
    if prot.is_typing()==True: #if we have a packet saying that someone is typing a message
        adr=prot.get_typing()
        print "typing:"+adr
        if g.is_ip(adrip)==False:
            g.add_ip(adrip)
        if g.ip(adrip).is_account(adr.strip())==False:
            g.ip(adrip).add_account(adr.strip())
            tvSn.add_if_not_sn_account_tree(adrip,adr.strip())
        #tvSn.create_sn_tree()
        #tvSn.update_sn_tree()
        #print ">>"+adrip+"->"+
        #g.ip(adrip).account(adr.strip()).add_to_speech("[scribing]")
                    
    if prot.is_msg()==True: #If we have a chat message
        if prot.is_msg_received():
            mail=prot.get_email_msg_sender()
            msg=prot.get_msg()
            if g.is_ip(adrip)==False: #does this IP already exists in the SnGui
                g.add_ip(adrip)
            if g.ip(adrip).account_id(0).is_contact(mail)==False: #does this contact exists
                g.ip(adrip).account_id(0).add_contact(mail)
                tvSn.add_if_not_sn_contact_tree(adrip,g.ip(adrip).account_id(0).account,mail)
            g.ip(adrip).account_id(0).contact(mail).add_to_speech(msg+'\n') #add the message to the contact
            tvSn.show()
            #tvSn.create_sn_tree()


def process_packet(pktlen, data, timestamp):
    if not data:
        return

    if data[12:14]=='\x08\x00':
        decoded=decode_ip_packet(data[14:])
        det_IP_packet(decoded['destination_address'])
        det_IP_packet(decoded['source_address'])
        det_elems_data(decoded['data'],decoded['source_address'],decoded['destination_address'])


def main(p):
    #SnInterf.gtk.timeout_add(100,function_tempo,p)#each 100 ms function_tempo is called
    gobject.timeout_add(100,function_tempo,p)#each 100 ms the packet function dispatch is called
    gobject.timeout_add(100,function_tempo_refresh)#each 100 ms shows the window with treeview
    SnInterf.gtk.main()


def function_tempo(p):
    p.dispatch(1, process_packet)
    return True


def function_tempo_refresh():
    tvSn.show()
    return True


if __name__=="__main__":
    global g,tvSn

    p = pcap.pcapObject()
    port_ecoute="port 1863"
    dev = "eth0"
    net, mask = pcap.lookupnet(dev)
    p.open_live(dev, 1600, 0, 100)
    p.setfilter(port_ecoute, 0, 0)
    g=SnGui.SnGui() #container for ip->account->contact
    tvSn=SnInterf.SnGtkWindow(g) #gtk window with the treeview
    prot=SnProtocol.SnProtocol() #filtering packets with msn protocol

    main(p)
    
#    try:
#        while fin==False:
#    except KeyboardInterrupt:
#        print '%s' % sys.exc_type
#        print 'shutting down'
#        print '%d packets received, %d packets dropped, %d packets dropped by interface' %  p.stats()
    

