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
        
class Chats(Model):
    identification = CharField(primary_key = True)
    user_id = CharField()
    text = CharField()
    out = BooleanField()    
    
    class Meta:
        database = ldb

class Main:    
    def __init__(self):
        print("init")
        
        version = "5"
        if not os.path.exists(data_dir + "/version"):
            print("Writing new database")
            open(data_dir + "/version", "w").write("0")
        checkversion = str(open(data_dir + "/version", "r").readlines()[0])
        if not version == checkversion:   
            print("Database version is incompatible with new version, recreating it")
            if os.path.exists(data_dir + "/data.db"): os.remove(data_dir + "/data.db")
            open(data_dir + "/version", "w").write(version)     
        
        ldb.connect()   
                
        try: ldb.create_tables([Info])
        except: print("Info table exists in ldb")  
        try: ldb.create_tables([Dialogs])
        except: print("Dialogs table exists in ldb")    
        try: ldb.create_tables([Chats])
        except: print("Chats table exists in ldb")     
        
        #try: migrate(local_migrator.add_column("Artikel", "groesse", CharField(default = "")))
        #except: print("Artikel:groesse:existiert schon")
           
        ldb.close()
        
        #pyotherside.send("changeFrame", "Dialogs")

        self.getDialogs()
                         
        self.tryConnect()
        
        self.ChatPartner = ""
        self.ChatPartnerID = ""
        self.ChatForceReload = False
        self.LastChatList = ""
        self.LastDialogList = ""
        
       
    def tryConnect(self):
        print("tryConnect")    
    
        api_id = 291651
        api_hash = '0f734eda64f8fa7dea8ed9558fd447e9'

        try:
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
        except: print("tryConnect ERROR No Network?")    
    
    def SetChatPartner(self, name, user_id):
        print("SetChatPartner(name: " + str(name) + ", user_id: " + str(user_id) + ")")
        self.ChatPartner = name
        self.ChatPartnerID = user_id
        self.ChatForceReload = True
        self.getChat()
     
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
    
    def getDialogs(self):
        print("getDialogs function in Main.py")
        
        Dialoge = []
        try: ldb.connect()
        except: True
        AllDialogs = Dialogs.select()
        ldb.close() 
        for dialog in AllDialogs:
            Dialoge.append({"name" : dialog.name, "user_id" : dialog.identification})
        
        print("pyotherside.send(antwortGetDialogs, " + str(Dialoge) + ")") 
        pyotherside.send("antwortGetDialogs", Dialoge)  
    
    def reloadDialogs(self):
        print("reloadDialogs function in Main.py")
        
        #print("self.client.get_me(): \n")
        #print(self.client.get_me())
        #print("")
        
        self.tryConnect()
        
        if True:#try:
            Dialoge = []
            for dialog in self.client.get_dialogs():
                dialog_name = utils.get_display_name(dialog.entity)
                dialog_identification = dialog.entity.id
                #print(dialog_identification)
                Dialoge.append({"name": dialog_name})
                #print("dialog.name " + str(dialog.name))
                try: ldb.connect()
                except: True
                query = Dialogs.select().where((Dialogs.name == str(dialog_name)))
                ldb.close()
                if not query.exists():
                    print("create Dialog entry")
                    NewDialog = Dialogs.create(name = dialog_name, identification = dialog_identification)
                    NewDialog.save()
                
            #print("Dialoge: " + str(Dialoge))
            if not self.LastDialogList == Dialoge:
                self.LastDialogList = Dialoge
                self.getDialogs()
                
            
        #except: print("getDialogs download failed")

    def sendChat(self, text):
        self.client.send_message(self.ChatPartner, text)
    
    def getChat(self):
        print("getChat")
        ChatList = []
        try: ldb.connect()
        except: True
        AllChats = Chats.select().where(Chats.user_id == self.ChatPartnerID)
        ldb.close()   
        for message in AllChats:    
            ChatList.append({"chattext": message.text, "out": message.out})
        
        if not self.LastChatList == ChatList or self.ChatForceReload:
            pyotherside.send("antwortGetChat", ChatList, self.ChatPartner)
            self.LastChatList = ChatList 
            self.ChatForceReload = False
        
    def reloadChat(self):
        print("reloadChat")
        try:
            for message in self.client.get_messages(self.ChatPartner, limit=1):
                try: ldb.connect()
                except: True
                print("message.id " + str(message.id))
                query = Chats.select().where(Chats.identification == str(message.id))
                ldb.close()
                if not query.exists():
                    print(message)
                    print(" ")
                
                    NewChat = Chats.create(identification = message.id, user_id = self.ChatPartnerID, text = message.message, out = message.out)
                    NewChat.save()
                    self.getChat() 
        except:
            print("reloadChat Error")  
            self.tryConnect()  

main = Main()
