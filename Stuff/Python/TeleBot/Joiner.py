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
        self.path = path
        self.client = client
        self.pause_time = 60
        #self.evaluate()

    def refresh(self):
        self.urls = []
        with open(self.path, 'r') as f:
            self.urls = reversed([x.replace('\n','') for x in f.readlines()])
        self.tried = []
        if os.path.exists('tried.txt'):
            with open('tried.txt','r') as file:
                self.tried =  [x.replace('\n','') for x in file.readlines()]
        self.skipped = []
        if os.path.exists('skipped.txt'):
            with open('skipped.txt','r') as file:
                self.skipped =  [x.replace('\n','') for x in file.readlines()]
        self.urls = [x for x in self.urls if x not in self.tried and x not in self.skipped]
        self.urls.reverse()
        print("Remaining links to try:", len(self.urls))

    def evaluate(self):
        self.refresh()
        joinchats = [x for x in self.urls if 'joinchat' in x]
        groups = [x for x in self.urls if not 'joinchat' in x]
        groups = []
        iteration = 0
        for g in joinchats:
            iteration += 1
            if iteration > 10:
                self.refresh()
                iteration = 0
            result = None
            try:
                result = self.client(CheckChatInviteRequest(g))
                print('{},{}'.format(g, result.stringify))
            except:
                try:
                    result = self.client(ImportChatInviteRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    try:
                        result = self.client(JoinChannelRequest(g))
                        print('{},{}'.format(g, result.stringify))
                    except:
                        #webbrowser.open(g, new=0, autoraise=True)
                        pass
                pass
            if not result is None:
                self.tried.append(g)
                with open('tried.txt','w') as file:
                    file.writelines(['{}\n'.format(x) for x in self.tried])
            else:
                self.skipped.append(g)
                with open('skipped.txt','w') as file:
                    file.writelines(['{}\n'.format(x) for x in self.skipped])
            for t in tqdm(range(self.pause_time)):
                time.sleep(1)
        for g in groups:
            #e = self.client.get_entity(g)
            result = None
            try:
                result = self.client(CheckChatInviteRequest(g))
                print('{},{}'.format(g, result.stringify))
            except:
                try:
                    result = self.client(ImportChatInviteRequest(g))
                    print('{},{}'.format(g, result.stringify))
                except:
                    try:
                        result = self.client(JoinChannelRequest(g))
                        print('{},{}'.format(g, result.stringify))
                    except:
                        #webbrowser.open(g, new=0, autoraise=True)
                        pass
                pass
            if not result is None:
                self.tried.append(g)
                with open('tried.txt','w') as file:
                    file.writelines(['{}\n'.format(x) for x in self.tried])
            else:
                self.skipped.append(g)
                with open('skipped.txt','w') as file:
                    file.writelines(['{}\n'.format(x) for x in self.skipped])
            self.refresh()
            for t in tqdm(range(self.pause_time)):
                time.sleep(1)

#JoinChannelRequest(g)
#ImportChatInviteRequest(g)
#CheckChatInviteRequest(g)
