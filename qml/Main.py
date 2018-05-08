#!/usr/bin/env python3
try: import pyotherside
except: True

import getpass

import os
import sys

import threading

import socket

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
import encodings
from telethon import TelegramClient, utils, events
#from telethon import *


from peewee import *

data_dir = "/home/" + getpass.getuser() + "/.local/share/telepygram.bluekenny"
if not os.path.exists(data_dir): os.mkdir(data_dir)
if not os.path.exists(data_dir + "/Pictures"): os.mkdir(data_dir + "/Pictures")
if not os.path.exists(data_dir + "/Media"): os.mkdir(data_dir + "/Media")
if not os.path.exists(data_dir + "/Pictures/Profiles"): os.mkdir(data_dir + "/Pictures/Profiles")
        
ldb = SqliteDatabase(data_dir + "/data.db")

class Uploads(Model): 
    text = CharField()
    chat_id = CharField()
    
    class Meta:
        database = ldb

class Dialogs(Model):
    identification = CharField(primary_key = True)
    name = CharField()
    status = CharField()
    dialog = CharField()
    
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
        
        version = "20"
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
        try: ldb.create_tables([Uploads])
        except: print("Uploads table exists in ldb")   
           
        ldb.close()
        
        self.ChatPartner = ""
        self.ChatPartnerID = ""
        self.ChatForceReload = False
        self.LastChatList = ""
        self.LastDialogList = ""
                
        self.getDialogs()
             
        threading.Thread(target = self.tryConnect)
           
       
    def tryConnect(self):
        print("tryConnect")    
    
        api_id = 291651
        api_hash = '0f734eda64f8fa7dea8ed9558fd447e9'

        self.client = TelegramClient(data_dir + "/telepygram.db", api_id, api_hash)
         
        self.phoneNumber = ""
            
        print("Connect to Telegram")
        try: isConnected = self.client.connect()
        except: isConnected = False      
            
        if isConnected:
            pyotherside.send("onlineStatus", True)
            
            isAuthorized = self.client.is_user_authorized()
            print("Authorized: " + str(isAuthorized))

            if not isAuthorized:
                pyotherside.send("changeFrame", "Phone")
                print("pyotherside.send(changeFrame, Phone)")
            
            return True
        else: 
            pyotherside.send("onlineStatus", False)
            return False
    
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
        
        if not AllDialogs.exists():
            Dialoge.append({"name" : "LOADING\nPLEASE WAIT", "chat_identification" : "", "status" : "", "timestamp" : "", "data_dir" : data_dir})
        else:  
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
        
                Dialoge.append({"name" : dialog.name, "chat_identification" : dialog.identification, "status" : user_status, "timestamp" : lastonlinetime, "data_dir" : data_dir})
                        
                
        #print("pyotherside.send(antwortGetDialogs, " + str(Dialoge) + ")") 
        pyotherside.send("antwortGetDialogs", Dialoge)  
    
    def reloadDialogs(self):
        print("reloadDialogs function in Main.py")
        
        #print("self.client.get_me(): \n")
        #print(self.client.get_me())
        #print("")
 
        isConnect = self.tryConnect()
        
        if isConnect:
            Dialoge = []
            for dialog in self.client.get_dialogs():
                dialog_name = utils.get_display_name(dialog.entity)
                dialog_identification = dialog.entity.id
                try: dialog_status = dialog.entity.status
                except: dialog_status = "0"  
                
                #print(" ")
                #print(dialog_name)
                #print(dialog.entity)
                #print(" ")
                
                Dialoge.append({"name": dialog_name, "status" : dialog_status})
                try: ldb.connect()
                except: True
                query = Dialogs.select().where((Dialogs.identification == str(dialog_identification)))
                ldb.close()
                if not query.exists():
                    print("create Dialog entry " + dialog_name)
                    threading.Thread(target = self.downloadProfilePhoto, args = [dialog.entity])
                    NewDialog = Dialogs.create(name = dialog_name, identification = dialog_identification, status = dialog_status, dialog = str(dialog))
                    NewDialog.save()
                else:
                    # ToDO Test if changes
                    
                    #print("Dialog Changed " + dialog_name)
                    ChangedDialog = Dialogs(name = dialog_name, identification = dialog_identification, status = dialog_status, dialog = str(dialog))
                    ChangedDialog.save()
                    
                    # if no Picture
                    if not os.path.exists(data_dir + "/Pictures/Profiles/" + str(dialog_identification) + ".jpg"):
                        threading.Thread(target = self.downloadProfilePhoto, args = [dialog.entity])
                
            #print("Dialoge: " + str(Dialoge))
            if not self.LastDialogList == Dialoge:
                self.LastDialogList = Dialoge
                self.getDialogs()
            
        else: print("getDialogs failed, no connection")

    def deleteProfilePhoto(self, id):
        print("deleteProfilePhoto(" + str(id) + ")")
        if os.path.exists(data_dir + "/Pictures/Profiles/" + str(id) + ".jpg"):        
            os.remove(data_dir + "/Pictures/Profiles/" + str(id) + ".jpg")        
        
    def downloadProfilePhoto(self, Entity):
        print("Start downloadProfilePhoto")
        print(" ")
        print(Entity)
        isConnect = self.tryConnect()
        if isConnect:
            Image = self.client.download_profile_photo(Entity, file=data_dir + "/Pictures/Profiles/" + str(Entity.id), download_big=True)
            #if str(Image) == "None": self.deleteProfilePhoto(Entity.id)        
            print("Image: " + str(Image))
        else: print("downloadProfilePhoto failed no connection")

    def sendChat(self, message):
        try: ldb.connect()
        except: True
        MessageToSend = Uploads.create(text = message, chat_id = self.ChatPartnerID)
        MessageToSend.save()    
        ldb.close()
        self.getChat()
    
    def trySending(self):       
        isConnect = self.tryConnect()
        if isConnect:   
            try: ldb.connect()
            except: True     
            query = Uploads.select()
            for messages in query:
                print("Sending (" + str(messages.id) + "): " + str(messages.text))        
                try:
                    self.client.send_message(int(messages.chat_id), messages.text)
                    messages.delete().execute()
                except:
                    print("Error Sending")
            ldb.close()
        else: print("trySending failed, no connection")
        
    
    def getChat(self):
        print("getChat")
        ChatList = []
        try: ldb.connect()
        except: True
        AllChats = Chats.select().where(Chats.chat_id == self.ChatPartnerID).order_by(Chats.identification)
        
        if not AllChats.exists():
            ChatList.append({"chattext": "LOADING\nPLEASE WAIT", "out": True, "sender" : "Telepygram", "read" : False, "media" : "", "with_media" : False})
        else:
            for message in AllChats:    
                if message.media == "None": with_media = False
                else: with_media = True
                ChatList.append({"chattext": message.text, "out": message.out, "sender" : message.user_name, "read" : False, "media" : message.media, "with_media" : with_media})
        
        query = Uploads.select().where(Uploads.chat_id == self.ChatPartnerID).order_by(Uploads.id)
        ldb.close()  
        
        for MessageToUpload in query:
            ChatList.append({"chattext": MessageToUpload.text, "out": True, "sender" : "SENDING", "read" : True, "media" : ""})
        
        
        if not self.LastChatList == ChatList or self.ChatForceReload:
            pyotherside.send("antwortGetChat", ChatList, self.ChatPartner)
            self.LastChatList = ChatList 
            self.ChatForceReload = False
        else: 
            print("LastChatList = ChatList")
        
    def reloadChat(self, LoadNewMessages):
        print("reloadChat")
        try:
            print("LoadNewMessages: " + str(LoadNewMessages))
            if LoadNewMessages:            
                Messages = self.client.iter_messages(self.ChatPartner, limit=10)
            else:
                try: ldb.connect()
                except: True

                AllSavedMessages = Chats.select()  
                SavedMessagesList = []
                for msg in AllSavedMessages:
                    SavedMessagesList.append(msg.identification)            
                
                ldb.close()
                
                LastMessageLoaded = int(min(SavedMessagesList))
                Messages = self.client.iter_messages(self.ChatPartner, offset_id=LastMessageLoaded, limit=10)
                
            for message in Messages:
                try: ldb.connect()
                except: True
                print("message.id " + str(message.id))
                query = Chats.select().where(Chats.identification == str(message.id))
                ldb.close()
                if not query.exists():
                    print(message)
                    print(" ")
                    
                    #print("User Name :" + str(self.client.get_entity(message.from_id)))
                    names = []
                    try: user_firstname = str(self.client.get_entity(message.from_id).first_name)
                    except: user_firstname = self.ChatPartner
                    try: user_lastname = str(self.client.get_entity(message.from_id).last_name)
                    except: user_lastname = "None"
                    if not user_firstname == "None": names.append(user_firstname)
                    if not user_lastname == "None": names.append(user_lastname)
                    username = " ".join(names)
                    
                    
                    message_text = message.message
                    if message_text == None:
                        message_text = ""  
                        print("action " + str(message.action))
                        if "MessageActionChatJoinedByLink" in str(message.action):
                            message_text = "joined by invite link"
                        if "MessageActionChatAddUser" in str(message.action):
                            message_text = "joined"
                            
                    username_id = str(message.from_id)
                    #print("username_id: " + username_id)
                    
                    try: message_media = str(message.media)
                    except: message_media = "None"
                    if not message_media == "None":
                        print("message_media: " + str(message_media))
                        file = data_dir + "/Media/" + str(message.id)
                        file = self.client.download_media(message.media, file=file, progress_callback=None)
                        message_media = file
                    
                    NewChat = Chats.create(identification = message.id, chat_id = self.ChatPartnerID, user_name = username, user_id = username_id, text = message_text, out = message.out, media = message_media ,total_message = message)
                    NewChat.save()                  
                    
                    self.getChat()
                 
        except:
            print("reloadChat Error")  
            threading.Thread(target = self.tryConnect)
    
   
main = Main()
