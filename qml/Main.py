#!/usr/bin/env python3
try: import pyotherside
except: True

import getpass

import os
import sys

import threading

import modules.BlueFunc

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
    status = CharField()
    
    class Meta:
        database = ldb
        
class Chats(Model):
    identification = CharField(primary_key = True)
    chat_id = CharField()
    user_id = CharField()
    user_name = CharField()
    text = CharField()
    out = BooleanField()  
    media = CharField()  
    total_message = CharField()
    
    class Meta:
        database = ldb

class Main:    
    def __init__(self):
        print("init")
        
        version = "14"
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
           
        ldb.close()

        self.getDialogs()
             
        threading.Thread(target = self.tryConnect).start()
        
        self.ChatPartner = ""
        self.ChatPartnerID = ""
        self.ChatForceReload = False
        self.LastChatList = ""
        self.LastDialogList = ""
        
        if not os.path.exists(data_dir + "/Pictures"): os.mkdir(data_dir + "/Pictures")
        if not os.path.exists(data_dir + "/Pictures/Profiles"): os.mkdir(data_dir + "/Pictures/Profiles")
        
       
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
    
    def SetChatPartner(self, name, id):
        print("SetChatPartner(name: " + str(name) + ", " + str(id) + ")")
        self.ChatPartner = name
        self.ChatPartnerID = id
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
            user_status = dialog.status
            #UserStatusOffline(was_online=datetime.utcfromtimestamp(1525351401))
            if "UserStatusOnline" in user_status: #Online
                user_status = "green"
                lastonlinetime = ""
            else:
                if user_status == "UserStatusRecently()": # Was online Recently
                    user_status = "orange"
                    lastonlinetime = ""
                else:
                    print("User Status is " + str(user_status))
                    user_status = "red"
                    lastonlinetime = ""
                    if "UserStatusOffline" in dialog.status:
                        lastonlinetime = modules.BlueFunc.ElapsedTime(dialog.status.split("UserStatusOffline(was_online=datetime.utcfromtimestamp(")[-1].replace("))", ""))
            # t = threading.Thread(target = self.tryConnect)
            #  download_profile_photo(entity, file=None, download_big=True)
                        
            
            Dialoge.append({"name" : dialog.name, "chat_identification" : dialog.identification, "status" : user_status, "timestamp" : lastonlinetime, "data_dir" : data_dir})
        
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
                try: dialog_status = dialog.entity.status
                except: dialog_status = "0"  
                
                print(" ")
                print(dialog_name)
                print(dialog.entity)
                print(" ")
                
                Dialoge.append({"name": dialog_name})
                try: ldb.connect()
                except: True
                query = Dialogs.select().where((Dialogs.identification == str(dialog_identification)))
                ldb.close()
                if not query.exists():
                    print("create Dialog entry " + dialog_name)
                    threading.Thread(target = self.downloadProfilePhoto, args = [dialog.entity]).start()
                    NewDialog = Dialogs.create(name = dialog_name, identification = dialog_identification, status = dialog_status)
                    NewDialog.save()
                else:
                    # ToDO Test if changes
                    
                    print("Dialog Changed " + dialog_name)
                    ChangedDialog = Dialogs(name = dialog_name, identification = dialog_identification, status = dialog_status)
                    ChangedDialog.save()
                    
                    # if no Picture
                    if not os.path.exists(data_dir + "/Pictures/Profiles/" + str(dialog_identification) + ".jpg"):
                        threading.Thread(target = self.downloadProfilePhoto, args = [dialog.entity]).start()
                
            #print("Dialoge: " + str(Dialoge))
            if not self.LastDialogList == Dialoge:
                self.LastDialogList = Dialoge
                self.getDialogs()
                
            
        #except: print("getDialogs download failed")
    def downloadProfilePhoto(self, Entity):
        print("Start downloadProfilePhoto")
        Image = self.client.download_profile_photo(Entity, file=data_dir + "/Pictures/Profiles/" + str(Entity.id), download_big=True)
        print("Image: " + str(Image))

    def sendChat(self, text):
        self.client.send_message(self.ChatPartner, text)
    
    def getChat(self):
        print("getChat")
        ChatList = []
        try: ldb.connect()
        except: True
        AllChats = Chats.select().where(Chats.chat_id == self.ChatPartnerID).order_by(Chats.identification)
        ldb.close()   
        for message in AllChats:    
            ChatList.append({"chattext": message.text, "out": message.out, "sender" : message.user_name})
        
        if not self.LastChatList == ChatList or self.ChatForceReload:
            pyotherside.send("antwortGetChat", ChatList, self.ChatPartner)
            self.LastChatList = ChatList 
            self.ChatForceReload = False
        else: 
            print("LastChatList = ChatList")
        
    def reloadChat(self):
        print("reloadChat")
        if True:#try:
            for message in self.client.get_messages(self.ChatPartner, limit=10):
                try: ldb.connect()
                except: True
                print("message.id " + str(message.id))
                query = Chats.select().where(Chats.identification == str(message.id))
                ldb.close()
                if not query.exists():
                    print(message)
                    print(" ")

                    message_text = message.message
                    if message_text == None: message_text = " "                  
                    
                    print("User Name :" + str(self.client.get_entity(message.from_id)))
                    names = []
                    user_firstname = str(self.client.get_entity(message.from_id).first_name)
                    user_lastname = str(self.client.get_entity(message.from_id).last_name)
                    if not user_firstname == "None": names.append(user_firstname)
                    if not user_lastname == "None": names.append(user_lastname)
                    username = " ".join(names)
                    
                    try: message_media = str(message.media)
                    except: message_media = " "
                    print("message_media: " + str(message_media))
                    # download_media(message, file=None, progress_callback=None)
                    
                    NewChat = Chats.create(identification = message.id, chat_id = self.ChatPartnerID, user_name = username, user_id = message.from_id, text = message_text, out = message.out, media = message_media ,total_message = message)
                    NewChat.save()
                    self.getChat() 
        if False:#except:
            print("reloadChat Error")  
            self.tryConnect()  

main = Main()
