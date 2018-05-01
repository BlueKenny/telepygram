#!/usr/bin/env python3
try: import pyotherside
except: True

import os
import sys

if sys.version_info.major == 3:
    print("python Major version " + str(sys.version_info.major))
    if sys.version_info.minor == 6:
        print("python Minor version " + str(sys.version_info.minor))
        sys.path.append("modules/lib64/python3.6/site-packages/")
        sys.path.append("modules/lib/python3.6/site-packages/")
    if sys.version_info.minor == 4:
        print("python Minor version " + str(sys.version_info.minor))
        sys.path.append("modules/lib/python3.4/site-packages/")
        os.system("ls")
    
#from telethon import TelegramClient, utils
from telethon import *

from peewee import *

ldb = SqliteDatabase("data.db")

class Dialogs(Model):
    username = CharField(primary_key = True)
    name = CharField()
    
    class Meta:
        database = ldb

class Main:    
    def __init__(self):
        print("init")
        
        #self.MakeDesktopEntry()
        
        #self.Update()  
        
        ldb.connect()   
        
        try: ldb.create_tables([Dialogs])
        except: print("Dialogs table exists in ldb")     
        
        try: migrate(local_migrator.add_column("Artikel", "groesse", CharField(default = "")))
        except: print("Artikel:groesse:existiert schon")

        api_id = 291651
        api_hash = '0f734eda64f8fa7dea8ed9558fd447e9'

        self.client = TelegramClient('telepygram', api_id, api_hash)
        self.phoneNumber = ""

        isConnected = False
        while not isConnected:
            print("Waiting for connection")
            isConnected = self.client.connect()
            print("Connection: " + str(isConnected))

        isAuthorized = self.client.is_user_authorized()
        print("Authorized: " + str(isAuthorized))

        if not isAuthorized:
            pyotherside.send("changeFrame", "Phone")
            print("pyotherside.send(changeFrame, Phone)")
            
        try: self.getDialogs()
        except: True
        
        self.ChatPartner = ""
        self.LastChatList = ""
       
    def SetChatPartner(self, name):
        print("SetChatPartner(" + str(name) + ")")
        self.ChatPartner = name
    
    def Update(self):
        print("Update")
        os.system("git pull &")   
    
    def MakeDesktopEntry(self):
        print("MakeDesktopEntry")
        
        User = os.popen("echo $USER").readlines()[0].rstrip()
        
        Places = []
        if os.path.exists("/home/phablet"):
            Places.append("/home/phablet/.local/share/applications")
            #Places.append("/home/phablet/.config/autostart")
        else:
            Places.append(os.popen("echo $(xdg-user-dir DESKTOP)").readlines()[0].rstrip())
            #Places.append(os.popen("echo $HOME").readlines()[0].rstrip() + "/.config/autostart")
            Places.append(os.popen("echo $HOME").readlines()[0].rstrip() + "/.local/share/applications")
        
        for Desktop in Places:
            file = Desktop + "/telepygram.desktop"
            #os.system("rm " + file)
            if not os.path.exists(file):
                print("Write Desktop Entry")
                print("User: " + str(User))
                print("Desktop: " + str(Desktop))
                print("file: " + str(file))
                DesktopEntry = open(file, "a")
                DesktopEntry.write("[Desktop Entry]\n")
                DesktopEntry.write("Name=Telepygram\n")
                DesktopEntry.write("Path=/home/" + User + "/telepygram/\n")
                if User == "pi":# für raspberry
                    DesktopEntry.write("Exec=qmlscene -qt=qt5-arm-linux-gnueabihf /home/" + User + "/telepygram/Main.qml\n")
                else:
                    DesktopEntry.write("Exec=qmlscene /home/" + User + "/telepygram/Main.qml\n")
                DesktopEntry.write("Terminal=false\n")
                DesktopEntry.write("X-Ubuntu-Touch=true\n")
                DesktopEntry.write("Type=Application\n")
                DesktopEntry.write("StartupNotify=true\n")
                DesktopEntry.write("Icon=/home/" + User + "/telepygram/icon.png\n")
                 
                os.system("chmod +x " + file)
     
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
        
        print("self.client.get_me(): \n")
        print(self.client.get_me())
        print("")
        
        #ldb_connect()
        #Dialoge = []
        #AllDialogs = Dialogs.select()
        #for dialog in AllDialogs:
        #    Dialoge.append({"name" : dialog.name})
        #pyotherside.send("antwortGetDialogs", Dialoge)
        #ldb_close()        
        
        try:
            Dialoge = []
            for dialog in self.client.get_dialogs():
                name = utils.get_display_name(dialog.entity)
                Dialoge.append({"name": name})
            print("Dialoge: " + str(Dialoge))
            pyotherside.send("antwortGetDialogs", Dialoge)  
        except: print("getDialogs download failed")
        
        print("pyotherside.send(antwortGetDialogs, Dialoge)")

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
