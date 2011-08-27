#-*- coding: utf-8 -*-

from os import environ

rc_file = environ["HOME"] + "/.contactos"

class Contact():
    
    def __init__(self, data):
        
        self.nickname = data[0]
        self.number = data[1]
    
    def get_data(self, cod=0):
        if cod == 0:
            return (self.nickname, self.number)
        elif cod == 1:
            return self.nickname
        elif cod == 2:
            return self.number
        else:
            return None
            
    def set_number(self, number):
        
        self.number = number
    
    def set_nickname(self, nick):
        
        self.nickname = nick
    
    def __str__(self):
        return '''
                Apodo: %s
                Númbero: %s
            ''' % (self.nickname, self.number)

class Contacts_agenda():
    
    def __init__(self):
        
        self.contacts = {}
        
        self.users = [line.strip().split(";")
        for line in open(rc_file).readlines()
            if not "#" in line]
        
        
        for index, user in enumerate(self.users):
            contact = Contact(user)
            self.contacts[index] = contact
    
    def set_contact(self, data):
        
        contact = Contact(data)
        new_index = self.contacts.keys().pop() + 1
        self.contacts[new_index] = contact
        contact_file = open(rc_file, 'a')
        contact_file.write('%s;%s' % contact.get_data())
        contact_file.close()
        
            
    def modified_contact(self, index, data):
        
        contact = Contact(data)
        self.contacts[index] = contact
        
    
    def show_contacts(self):
        
        for key in self.contacts.iterkeys():
            print key, self.contacts[key]
    
    
