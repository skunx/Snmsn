#! /usr/bin/env python

'''
@author: Daouzli
'''

class SnGui(object):
    '''class containing the structure ip -> account -> contact'''
    def __init__(self):
        self.data = []
        '''list of ips'''

    def ip(self, ip):
        '''Retrieve an object IP.

        @param ip: the ip of the object to retrieve
        @return: the object ip ip if exists or else None

        '''
        for d in self.data:
            if d.ip == ip: return d
        return None

    def ip_id(self, idx):
        '''Retieve and object IP by its id.

        @param idx: index of the IP
        @return: the object ip to retrieve if exists or else None

        '''
        if len(self.data) > idx:
            return self.data[idx]
        return None

    def list_ips(self):
        '''Retrieve the list of ips

        @return: list of ip

        '''
        return [d.ip for d in self.data]

    def add_ip(self, ip):
        '''Add an ip if doesn't already exist

        @param ip: IP object to add

        '''
        if self.is_ip(ip) == False:
            self.data.append(Sn_IP(ip))

    def is_ip(self, ip):
        '''Check if an IP exists.

        @param: ip to considere
        @return: True if exists or False

        '''
        return True if len([d.data for d in self.data if d.ip == ip]) > 0 else False



class Sn_IP():
    ''' This class contains the IP adress of the network that is observed '''
    def __init__(self, ip):
        self.data = []
        '''list of accounts'''
        self.ip = ip

    def __str__(self):
        return self.ip

    def account(self, account):
        '''Retrieve an account.

        @param account: account name to search
        @return: the account object of this ip if exists or else None

        '''
        for d in self.data:
            if d.account == account: return d
        return None

    def account_id(self, idx):
        '''Retrieve an account by its index

        @param idx: index of the account to retrieve
        @return: the object account if exists or else None

        '''
        if len(self.data) > idx:
            return self.data[idx]
        return None

    def list_accounts(self):
        '''Retrieve the list of accounts

        @return: the list of accounts of this ip

        '''
        return [d.account for d in self.data]

    def add_account(self, account):
        '''Add an account if doesn't already exist.

        @param account: the account to add

        '''
        if self.is_account(account) == False:
            self.data.append(Sn_Account(account))

    def is_account(self, account):
        '''Check if an account exists.

        @param account: the account to search
        @return: True if account exists for this ip or else False

        '''
        return True if len([d.data for d in self.data if d.account == account]) > 0 else False



class Sn_Account():
    '''This class contains the msn account used with a particular IP adress

    '''
    def __init__(self, account):
        self.data = []
        '''list of contacts'''
        self.account = account

    def __str__(self):
        return self.account

    def contact(self, contact):
        '''Retieve a contact.

        @param contact: the contact to retrieve
        @return: the contact of this account if exists or else None

        '''
        for d in self.data:
            if d.contact == contact: return d
        return None

    def contact_id(self, idx):
        '''Retrieve a contact by its index.

        @param idx: index of the contact
        @return: the contact if exists or else None

        '''
        if len(self.data) > idx:
            return self.data[idx]
        return None

    def list_contacts(self):
        '''"Retrieve the list of contacts.

        @return: the list of contacts of this account

        '''
        return [d.contact for d in self.data]

    def add_contact(self, contact):
        '''Add a contact to this account

        @param contact: contact to add if doesn't already exist

        '''
        if self.is_contact(contact) == False:
           self.data.append(Sn_Contact(contact))

    def is_contact(self, contact):
        '''Check if a contact exists for this account.

        @param contact: contact to search
        @return: True or False
        @rtype: boolean

        '''
        return True if len([d for d in self.data if d.contact == contact]) > 0 else False


class Sn_Contact():
    '''This class contains the msn active contact for a particular account

    '''
    def __init__(self, contact):
        self.contact = contact
        self.speech = ""

    def __str__(self):
        return self.contact

    def new_speech(self, speech=""):
        '''Initializes the speech between the account and this contact

        @param speech: text to set or "" if no argument

        '''
        self.speech = speech

    def add_to_speech(self, speech):
        '''Add a text to the speech between the account and this contact

        @param speech: text to add

        '''
        self.speech += speech


if __name__ == "__main__":
    g = SnGui()
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
    if g.is_ip("192.168.0.10") == True:
       print "ya 192.168.0.10!!"
    else:
       print "ya pas :("
    g.ip("192.168.0.10").account("didi@hotmail.com").contact("coco").new_speech("conversation tres super\nyeah!\n")
    g.ip("192.168.0.10").account("didi@hotmail.com").contact("coco").add_to_speech("ah ouai carrement grave :p!\n")
    print g.ip("192.168.0.10").account("didi@hotmail.com").contact("coco").speech
    g.ip("192.168.0.10").add_account("popo@hotmail.com")
    print g.ip("192.168.0.10").account("popo@hotmail.com").account
#    g.add_acc_to_ip("192.168.0.10", "popo@hotmail.com")
#    g.add_acc_to_ip("192.168.0.10", "didi@hotmail.com")
#    g.add_contact_to_acc_ip("192.168.0.10", "didi@hotmail.com", "coco")
#    g.add_contact_to_acc_ip("192.168.0.10", "didi@hotmail.com", "cocos")
#    g.add_contact_to_acc_ip("192.168.0.10", "didi@hotmail.com", "coco")
#    print g.list_acc_per_ip("192.168.0.10")

#    print g.data[0].data[1].acc


