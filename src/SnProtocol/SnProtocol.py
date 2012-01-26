#! /usr/bin/env python

'''
@author: Daouzli
'''

import re

class SnProtocol:
    """ SnProtocol: class containing functions to filter the packets with msn protocol"""
    def __init__(self):
        self.data=''
        self.trid=0
        
    def set_data(self,data):
        """ set_data(data): use data for processing"""
        self.data=data
    
    def is_email(self):
        """ is_email(): return True if data contains the character @ or else False"""
        try:
            self.data.index('@')
            return True
        except:
            return False
    
    def get_email(self):
        """ get_email(): return a list of emails if there are emails in self.data"""
        email=re.findall(r'([\w\.\-]+@[\w\.\-]+)',self.data)
        return email
    
    def is_msg_cmd(self):
        """ is_msg(): return True if the self.data contains the MSG command"""
        try:
            self.data.index('MSG')
            return True
        except:
            return False
            
    def get_msg_data(self):
        """ get_msg(): return a dictionary containing the message and informations
                       keys are: trid, code, email, msg """
        dicmsg={trid:None,code:None,email:None,msg:None}
        return dicmsg

    def is_msg(self):
        """ is_msg(): return True if the self.data is a message or else False"""
        try:
            self.data.index('text/plain')
            return True
        except:
            return False
            
    def get_msg(self):
        """ get_msg(): return the sent/received message """
        print self.data.split()
        idx=self.data.index('text/plain')
        data=self.data[idx:]
        idx=data.index('\r\n\r\n')
        data=data[idx:].strip()
        return data

    def is_msg_received(self):
        """is_msg_received(): return True if the message is received or else False (use is_msg() before)"""
        idx=self.data.index('MSG')
        data=self.data[idx:]
        try: 
            data.split()[1].index('@')
            return True
        except:
            return False
            
    def get_email_msg_sender(self):
        """get_email_msg_sender(): return the email of the sender of the received message (use is_msg_received() before)"""
        idx=self.data.index('MSG')
        data=self.data[idx:]
        return data.split()[1]
        
    def get_trid(self):
        pass
        
    def is_typing(self):
        """is_typing(): return True if a user account is typing or else False"""
        if "text/x-msmsgscontrol" in self.data.split():
            return True
        else:
            return False
        
    def get_typing(self):
        """get_typing(): return email of the user account typing (use is_typing() before)"""
        idx=self.data.split().index("TypingUser:")
        typing=self.data.split()[idx+1]
        return typing

if __name__=="__main__":
    pass

