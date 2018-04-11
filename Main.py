#!/usr/bin/env python3
import pyotherside

try:
    from telethon import TelegramClient, utils
except:
    import os
    print("Module Telethon, not installed, starting Installation...")
    os.system("pip3 install --user telethon")
    print("Module Telethon Installed, please restart APP...")
    from telethon import TelegramClient, utils

# Telethon DOCS
# http://telethon.readthedocs.io/en/latest/extra/basic/creating-a-client.html#creating-a-client

# own infos : client.get_me()


class Main:    
    def __init__(self):
        print("init")
        
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
        
    def setPhoneNumber(self, phoneNumber):
        self.phoneNumber = phoneNumber
        print("setPhoneNumber(" + str(phoneNumber) + ")")
        self.client.send_code_request(phoneNumber)
        pyotherside.send("changeFrame", "Code")
        
    def setPhoneCode(self, phoneCode):
        print("setPhoneCode(" + str(phoneCode) + ")")
        self.client.sign_in(self.phoneNumber, phoneCode)  
        pyotherside.send("changeFrame", "Dialogs")
        
    #phone_number = input("Enter your phone number\nIn international format please\n")
    #client.send_code_request(phone_number)
    #authorized_code = input("Please enter code:\n")
    #me = client.sign_in(phone_number, authorized_code)  
    
    
#print(client.get_me())


#client.send_message("me", "Telepygram\n")


#for dialog in client.get_dialogs(limit=20):
#    print("\n")
#    print(utils.get_display_name(dialog.entity), dialog.message) # dialog.message prints the last mesage
#    for message in client.get_messages(dialog.entity):
#        print("\n")
#        print(message)


main = Main()
