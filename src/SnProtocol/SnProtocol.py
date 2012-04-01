#! /usr/bin/env python

'''
@author: Daouzli
'''

import re

class SnProtocol:
    """Class containing functions to filter the packets with msn protocol"""

    def __init__(self):
        self.data = ''
        self.trid = 0


    def set_data(self, data):
        """Set the data to proceed

        @param data: the data

        """
        self.data = data


    def is_email(self):
        """Check if data contains the character @

        @return: True if contains @ or False
        @rtype: boolean

        """
        try:
            self.data.index('@')
            return True
        except:
            return False

    def get_email(self):
        """Get a list of emails if there are emails in self.data

        @return: the emails list
        @rtype: list

        """
        email = None
        if self.is_email():
            email = re.findall(r'([\w\.\-]+@[\w\.\-]+)', self.data)
        return email


    def is_msg_cmd(self):
        """Check if the self.data contains the MSG command

        @return True or False
        @rtype: boolean

        """
        try:
            self.data.index('MSG')
            return True
        except:
            return False


    def get_msg_data(self):
        """Get the message and informations

        @return: a dictionary containing the message and informations.
        keys are: trid, code, email, msg
        @rtype: dictionary

        """
        dicmsg = {trid:None, code:None, email:None, msg:None}
        return dicmsg


    def is_msg(self):
        """Check if the stored data is a message

        @return: True or False
        @rtype: boolean

        """
        try:
            self.data.index('text/plain')
            return True
        except:
            return False

    def get_msg(self):
        """Get the sent/received message

        @return: the message

        """
        data = None
        if self.is_msg():
            print self.data.split()
            idx = self.data.index('text/plain')
            data = self.data[idx:]
            idx = data.index('\r\n\r\n')
            data = data[idx:].strip()
        return data


    def is_msg_received(self):
        """Check if the message is received. You must use is_msg() before.

        @return: True or False
        @rtype: boolean

        """
        idx = self.data.index('MSG')
        data = self.data[idx:]
        try:
            data.split()[1].index('@')
            return True
        except:
            return False


    def get_email_msg_sender(self):
        """Get the email of the sender of the received message.

        @return: the email

        """
        email = None
        if self.is_msg_received():
            idx = self.data.index('MSG')
            data = self.data[idx:]
            email = data.split()[1]
        return email

    def get_trid(self):
        pass


    def is_typing(self):
        """Check if a user account is typing.

        @return: True or False
        @rtype: boolean

        """
        if "text/x - msmsgscontrol" in self.data.split():
            return True
        else:
            return False


    def get_typing(self):
        """Get email of the user account typing.

        @return: the email

        """
        typing = None
        if self.is_typing():
            idx = self.data.split().index("TypingUser:")
            typing = self.data.split()[idx + 1]
        return typing

if __name__ == "__main__":
    pass

