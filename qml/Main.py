#!/usr/bin/env python3
try: import pyotherside
except: True

import getpass


import os
import sys

if sys.version_info.major == 3:
    print("python Major version " + str(sys.version_info.major))
    if sys.version_info.minor == 6:
        print("python Minor version " + str(sys.version_info.minor))
        sys.path.append("modules/lib64/python3.6/site-packages/")
        sys.path.append("modules/lib/python3.6/site-packages/")
        sys.path.append("qml/modules/lib64/python3.6/site-packages/")
        sys.path.append("qml/modules/lib/python3.6/site-packages/")
    if sys.version_info.minor == 4:
        print("python Minor version " + str(sys.version_info.minor))
        sys.path.append("modules/lib/python3.4/site-packages/")
        sys.path.append("qml/modules/lib/python3.4/site-packages/")
    
import typing
from telethon import TelegramClient, utils
#from telethon import *

from peewee import *

data_dir = "/home/" + getpass.getuser() + "/.local/share/telepygram.bluekenny"
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
ldb = SqliteDatabase(data_dir + "/data.db")

class Dialogs(Model):
    identification = CharField(primary_key = True)
    name = CharField()
    
    class Meta:
        database = ldb

class Main:    
    def __init__(self):
        print("init")
        
        ldb.connect()   
        
        try: ldb.create_tables([Dialogs])
        except: print("Dialogs table exists in ldb")     
        
        #try: migrate(local_migrator.add_column("Artikel", "groesse", CharField(default = "")))
        #except: print("Artikel:groesse:existiert schon")
           
        ldb.close()
         
        #self.tryConnect()
        
        try: self.getDialogs()
        except: True
        
        self.ChatPartner = ""
        self.LastChatList = ""
       
    def tryConnect(self):
        api_id = 291651
        api_hash = '0f734eda64f8fa7dea8ed9558fd447e9'

        self.client = TelegramClient(data_dir + "/telepygram.db", api_id, api_hash)
        self.phoneNumber = ""

        print("Waiting for connection")
        isConnected = self.client.connect()
        print("Connection: " + str(isConnected))

        isAuthorized = self.client.is_user_authorized()
        print("Authorized: " + str(isAuthorized))

        if not isAuthorized:
            pyotherside.send("changeFrame", "Phone")
            print("pyotherside.send(changeFrame, Phone)")
    
    def SetChatPartner(self, name):
        print("SetChatPartner(" + str(name) + ")")
        self.ChatPartner = name
     
    def setPhoneNumber(self, phoneNumber):
        self.phoneNumber = phoneNumber
        print("setPhoneNumber(" + str(phoneNumber) + ")")
        self.client.send_code_request(phoneNumber)
        pyotherside.send("changeFrame", "Code")
        print("pyotherside.send(changeFrame, Code)")
        
    def setPhoneCode(self, phoneCode):
        print("setPhoneCode(" + str(phoneCode) + ")")
        self.client.sign_in(self.phoneNumber, phoneCode)  
        pyotherside.send("changeFrame", "Dialogs")
        print("pyotherside.send(changeFrame, Dialogs)")
        self.getDialogs()
        
    #phone_number = input("Enter your phone number\nIn international format please\n")
    #client.send_code_request(phone_number)
    #authorized_code = input("Please enter code:\n")
    #me = client.sign_in(phone_number, authorized_code)  
    
    def getDialogs(self):
        print("getDialogs function in Main.py")
        
        ldb.connect()
        Dialoge = []
        AllDialogs = Dialogs.select()
        for dialog in AllDialogs:
            Dialoge.append({"name" : dialog.name})
        ldb.close() 
        
        print("pyotherside.send(antwortGetDialogs, Dialoge)") 
        pyotherside.send("antwortGetDialogs", Dialoge)  
    
    def reloadDialogs(self):
        print("reloadDialogs function in Main.py")
        
        #print("self.client.get_me(): \n")
        #print(self.client.get_me())
        #print("")
        
        self.tryConnect()
        
        ldb.connect()    
        
        if True:#try:
            Dialoge = []
            for dialog in self.client.get_dialogs():
                dialog_name = utils.get_display_name(dialog.entity)
                dialog_identification = dialog.entity.id
                print(dialog_identification)
                Dialoge.append({"name": dialog_name})
                print("dialog.name " + str(dialog.name))
                query = Dialogs.select().where((Dialogs.name == str(dialog_name)))
                if not query.exists():
                    print("create Dialog entry")
                    NewDialog = Dialogs.create(name = dialog_name, identification = dialog_identification)
                    NewDialog.save()
                
            print("Dialoge: " + str(Dialoge))
            
        #except: print("getDialogs download failed")
        
        ldb.close()    

    def sendChat(self, text):
        self.client.send_message(self.ChatPartner, text)
    
    def getChat(self):
        ChatList = []
        for message in self.client.get_messages(self.ChatPartner, limit=20):
            print(message)
            if True:#if not message.out:
                ChatList.append({"chattext": message.message, "out": message.out})
                
        if not self.LastChatList == ChatList:
            pyotherside.send("antwortGetChat", ChatList, self.ChatPartner)
            self.LastChatList = ChatList

#client.send_message("me", "Telepygram\n")


#for dialog in client.get_dialogs(limit=20):
#    print("\n")
#    print(utils.get_display_name(dialog.entity), dialog.message) # dialog.message prints the last mesage
#    for message in client.get_messages(dialog.entity):
#        print("\n")
#        print(message)


main = Main()
