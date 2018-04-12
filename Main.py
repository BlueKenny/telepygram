#!/usr/bin/env python3
import pyotherside

import os

try:
    from telethon import TelegramClient, utils
except:
    import os
    print("Module Telethon, not installed, starting Installation...")
    os.system("pip3 install --user typing") # typing is needed in python3.4 for telethon
    os.system("pip3 install --user telethon")
    print("Module Telethon Installed, please restart APP...")
    from telethon import TelegramClient, utils

# Telethon DOCS
# http://telethon.readthedocs.io/en/latest/extra/basic/creating-a-client.html#creating-a-client

# own infos : client.get_me()


class Main:    
    def __init__(self):
        print("init")
        
        self.MakeDesktopEntry()
        
        self.Update()  
        
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
        
    #phone_number = input("Enter your phone number\nIn international format please\n")
    #client.send_code_request(phone_number)
    #authorized_code = input("Please enter code:\n")
    #me = client.sign_in(phone_number, authorized_code)  
    
    def getDialogs(self):
        print("getDialogs")
        
        print("self.client.get_me(): \n")
        print(self.client.get_me())
        print("")
        
        Dialoge = []
        for dialog in self.client.get_dialogs():
            name = utils.get_display_name(dialog.entity)
            Dialoge.append({"name": name})
        print("Dialoge: " + str(Dialoge))
        pyotherside.send("antwortGetDialogs", Dialoge)
        print("pyotherside.send(antwortGetDialogs, Dialoge)")


#client.send_message("me", "Telepygram\n")


#for dialog in client.get_dialogs(limit=20):
#    print("\n")
#    print(utils.get_display_name(dialog.entity), dialog.message) # dialog.message prints the last mesage
#    for message in client.get_messages(dialog.entity):
#        print("\n")
#        print(message)


main = Main()
