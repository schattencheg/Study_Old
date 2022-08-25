from telethon import TelegramClient, sync, events
from telethon import functions, types
from telethon.tl.types import InputMessagesFilterVideo, InputMessagesFilterUrl, InputMessagesFilterContacts
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
import os 
from datetime import datetime
import time
from tqdm import tqdm
from pathvalidate import sanitize_filepath
import numpy as np
import random
import webbrowser
import shutil

class Joiner:
    def __init__(self, client, path = None, urls = []):
        self.client = client
        self.urls = []
        if path is None:
            if len(urls) == 0:
                return
            self.urls = urls
        else:
            with open(path, 'r') as f:
                self.urls = reversed([x.replace('\n','') for x in f.readlines()])
        self.tried = []
        if os.path.exists('tried.txt'):
            with open('tried.txt','r') as file:
                self.tried =  [x.replace('\n','') for x in file.readlines()]
        self.urls = [x for x in self.urls if x not in self.tried]
        self.evaluate()

    def evaluate(self):
        joinchats = [x for x in self.urls if 'joinchat' in x]
        groups = [x for x in self.urls if not 'joinchat' in x]
        for g in groups:
            #e = self.client.get_entity(g)
            i = 1
            try:
                result = self.client(CheckChatInviteRequest(g))
                print('{},{}'.format(g, result.stringify))
            except:
                webbrowser.open(g, new=0, autoraise=True)
                pass
            if False:
                try:
                    result = self.client(JoinChannelRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    webbrowser.open(g, new=0, autoraise=True)
                    pass
                try:
                    result = self.client(ImportChatInviteRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    webbrowser.open(g, new=0, autoraise=True)
                    pass
                try:
                    result = self.client(CheckChatInviteRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    webbrowser.open(g, new=0, autoraise=True)
                    pass
            self.tried.append(g)
            with open('tried.txt','w') as file:
                file.writelines(['{}\n'.format(x) for x in self.tried])
            time.sleep(120)
        for g in joinchats:
            #e = self.client.get_entity(g)
            i = 1
            try:
                result = self.client(CheckChatInviteRequest(g))
                print('{},{}'.format(g, result.stringify))
            except:
                webbrowser.open(g, new=0, autoraise=True)
                pass
            if False:
                try:
                    result = self.client(JoinChannelRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    webbrowser.open(g, new=0, autoraise=True)
                    pass
                try:
                    result = self.client(ImportChatInviteRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    webbrowser.open(g, new=0, autoraise=True)
                    pass
                try:
                    result = self.client(CheckChatInviteRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    webbrowser.open(g, new=0, autoraise=True)
                    pass
            self.tried.append(g)
            with open('tried.txt','w') as file:
                file.writelines(['{}\n'.format(x) for x in self.tried])
            time.sleep(120)

#JoinChannelRequest(g)
#ImportChatInviteRequest(g)
#CheckChatInviteRequest(g)
