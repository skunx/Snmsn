#! /usr/bin/env python

'''
@author: Daouzli
'''

class Sn_Gui():
    """class containing the structure ip->account->contact"""
    def __init__(self):
        self.donnee=[] #list of ips

    def ip(self,ip):
        """ip(ip): return the object ip ip if exists or else None"""
        for d in self.donnee:
            if d.ip==ip: return d
        return None

    def ip_id(self,id):
        """ip_id(id): return the object ip of index id if exists or else None"""
        if len(self.donnee)>id:
            return self.donnee[id]
        return None

    def list_ips(self):
        """"list_ips(): return the list of ips"""
        return [d.ip for d in self.donnee]

    def add_ip(self,ip):
        """add_ip(ip): add ip if doesn't already exist"""
        if self.is_ip(ip)==False:
            self.donnee.append(Sn_IP(ip))
        
    def is_ip(self,ip):
        return True if len([d.donnee for d in self.donnee if d.ip==ip])>0 else False



class Sn_IP():
    """ This class contains the IP adress of the network that is observed """
    def __init__(self,ip):
        self.donnee=[] #list of accounts
        self.ip=ip

    def __str__():
        return self.ip

    def account(self,account):
        """account(account): return the object account account of this ip if exists or else None"""
        for d in self.donnee:
            if d.account==account: return d
        return None

    def account_id(self,id):
        """account_id(id): return the object account of index id if exists or else None"""
        if len(self.donnee)>id:
            return self.donnee[id]
        return None

    def list_accounts(self):
        """"list_accounts(): return the list of accounts of this ip"""
        return [d.account for d in self.donnee]

    def add_account(self,account):
        """add_account(account): add account to this ip if doesn't already exist"""
        if self.is_account(account)==False:
            self.donnee.append(Sn_Account(account))
        
    def is_account(self,account):
        """is_account(account): return True if account exists for this ip or else False"""
        return True if len([d.donnee for d in self.donnee if d.account==account])>0 else False
    
   

class Sn_Account():
    """ This class contains the msn account used with a particular IP adress """
    def __init__(self,account):
        self.donnee=[] #list of contacts
        self.account=account
        
    def __str__():
        return self.account

    def contact(self,contact):
        """contact(contact): return the object contact contact of this account if exists or else None"""
        for d in self.donnee:
            if d.contact==contact: return d
        return None

    def contact_id(self,id):
        """contact_id(id): return the object contact of index id if exists or else None"""
        if len(self.donnee)>id:
            return self.donnee[id]
        return None

    def list_contacts(self):
        """"list_contacts(): return the list of contacts of this account"""
        return [d.contact for d in self.donnee]

    def add_contact(self,contact):
        """add_contact(contact): add contact to this account if doesn't already exist"""
        if self.is_contact(contact)==False:
           self.donnee.append(Sn_Contact(contact))

    def is_contact(self,contact):
        """is_contact(contact): return True if contact exists for this account else False"""
        return True if len([d for d in self.donnee if d.contact==contact])>0 else False


class Sn_Contact():
    """ This class contains the msn active contact for a particular account """
    def __init__(self,contact):
        self.contact=contact
        self.speech=""
        
    def __str__():
        return self.contact

    def new_speech(self,speech=""):
        """new_speech(speech=""): initialize the speech between the account and this contact to speech or \"\" if no argument """
        self.speech=speech

    def add_to_speech(self,speech):
        """add_to_speech(speech=""): add speech to the speech between the account and this contact """
        self.speech=self.speech+speech


if __name__=="__main__":
    g=Sn_Gui()
    g.add_ip("192.168.0.10")
    g.add_ip("192.168.0.3")
    g.ip("192.168.0.10").add_account("popo@hotmail.com")
    g.ip("192.168.0.10").add_account("didi@hotmail.com")
    g.ip("192.168.0.10").account("didi@hotmail.com").add_contact("coco")
    print g.ip("192.168.0.10").account("didi@hotmail.com").is_contact("cocos")
    g.ip("192.168.0.10").account("didi@hotmail.com").add_contact("cocos")
    g.ip("192.168.0.10").account("didi@hotmail.com").add_contact("coco")
    print g.ip("192.168.0.10").account("didi@hotmail.com").is_contact("cocos")
    print g.list_ips()
    print g.ip("192.168.0.10").list_accounts()
    print g.ip("192.168.0.3").list_accounts()
    g.add_ip("192.168.0.10")
    if g.is_ip("192.168.0.10")==True:
       print "ya 192.168.0.10!!" 
    else:
       print "ya pas :("
    g.ip("192.168.0.10").account("didi@hotmail.com").contact("coco").new_speech("conversation tres super\nyeah!\n")
    g.ip("192.168.0.10").account("didi@hotmail.com").contact("coco").add_to_speech("ah ouai carrement grave :p!\n")
    print g.ip("192.168.0.10").account("didi@hotmail.com").contact("coco").speech
    g.ip("192.168.0.10").add_account("popo@hotmail.com")
    print g.ip("192.168.0.10").account("popo@hotmail.com").account
#    g.add_acc_to_ip("192.168.0.10","popo@hotmail.com")
#    g.add_acc_to_ip("192.168.0.10","didi@hotmail.com")
#    g.add_contact_to_acc_ip("192.168.0.10","didi@hotmail.com","coco")
#    g.add_contact_to_acc_ip("192.168.0.10","didi@hotmail.com","cocos")
#    g.add_contact_to_acc_ip("192.168.0.10","didi@hotmail.com","coco")
#    print g.list_acc_per_ip("192.168.0.10")

#    print g.donnee[0].donnee[1].acc
    
    
