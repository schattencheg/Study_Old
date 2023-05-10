from telethon import TelegramClient, sync, events
from telethon import functions, types
from telethon.tl.types import InputMessagesFilterVideo, InputMessagesFilterUrl, InputMessagesFilterContacts
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
import os 
from datetime import datetime
import time
from tqdm import tqdm
from pathvalidate import sanitize_filepath
import numpy as np
import random
import webbrowser
import shutil
from Joiner import Joiner
from threading import Thread
#import logging
#logging.basicConfig(level=logging.DEBUG)

class MyClient(TelegramClient):
    def __init__(self):
        #self.EraseAllFolders()
        if False:# or True:
            api_id = 10966915
            api_hash = '4b44f632cfdfc6171ed0456ad7b8497a'
            self.client = TelegramClient('session_name', api_id, api_hash)
            self.client.connect()
            j = Joiner(self.client, 'urls.txt')        
            j.evaluate()
            #self.thread = Thread(target=j.evaluate)
            #self.thread.start()

        while True:
            #continue
            api_id = 10966915
            api_hash = '4b44f632cfdfc6171ed0456ad7b8497a'
            self.client = TelegramClient('session_name', api_id, api_hash)
            self.client.connect()

            with open('urls.txt','r', encoding="utf-8") as f:
                self.urls = f.readlines()
            with open('sent.txt','r', encoding="utf-8") as f_sent:
                self.sent_requests = [x.replace('\n','') for x in f_sent.readlines()]
            with open('contacts.txt','r', encoding="utf-8") as f:
                self.contacts = f.readlines()
            self.urls_dict = dict()
            self.thumb_dict = dict()
            self.contacts = []        
            self.GetChats()
            self.client.disconnect()
            time.sleep(360)

    def EraseAllFolders(self):
        path = 'Output\\Channels'
        onlydirs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        for dir in onlydirs:
            self.EraseThumbnails(dir)

    def EraseThumbnails(self, channel_name):
        if '\\' in channel_name:
            channel_name = channel_name.replace('\\','_').replace(':','_')
        path = sanitize_filepath(os.path.join('Output\\Channels',sanitize_filepath(channel_name)))
        if os.path.exists(path):
            onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.getsize(os.path.join(path, f)) > 0]
            onlydirs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for f in onlyfiles:
                with open(os.path.join(path,f), 'w') as file:
                    file.write('')
        path = path + '_long'
        if os.path.exists(path):
            onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.isfile(os.path.join(path, f))]
            for f in onlyfiles:
                with open(os.path.join(path,f), 'w') as file:
                    file.write('')

    def GetChats(self):
        dialogs = self.client.iter_dialogs()
        channels = [x for x in dialogs if x.is_group]
        channels = [x for x in dialogs if x.is_channel or x.is_group]
        mes_count = dict([[d.id, d.unread_count] for d in dialogs if not getattr(d.entity, 'is_private', False) and d.unread_count != 0])
        sent_requests = [x.replace('\n','') for x in self.urls]
        random.shuffle(channels)
        print('Total chats: {}'.format(len(channels)))
        prev_chat_name = ''
        total_downloaded = 0
        #channels = [c for c in channels if 'мпя' in c_name.lower()]
        for c in tqdm(channels):
            c_name = c.name
            #continue
            if c_name == 'c:\\prn\\ero':
                c_name = 'c_prn_ero'
            if 'мпябнб' in c_name:
                stop = True
            if prev_chat_name != '':
                self.EraseThumbnails(prev_chat_name)
            prev_chat_name = c_name.lower()
            self.EraseThumbnails(c_name.lower())
            try:
                if 'таганрог' in c_name.lower() or 'торшер'  in c_name.lower() or 'тикток'  in c_name.lower() or 'tiktok' in c_name.lower() or 'ополч' in c_name.lower():
                    continue
                #if c.entity.restricted:
                #    continue
                #print('{}\n\'{}\' : {}\n'.format(datetime.now(),c_name, mes_count[c.id]))
                
                path = sanitize_filepath(os.path.join('Output\\Channels',c_name))
                if not os.path.exists(path):
                    os.makedirs(path)
                if not c_name in self.thumb_dict:
                    self.thumb_dict[c_name] = []
                lim = None
                if False or c.id in mes_count:
                    lim = mes_count[c.id]
                    if lim < 1:
                        continue
                mes = self.client.get_messages(c, limit= lim, filter=InputMessagesFilterVideo)
                allmes = self.client.get_messages(c, limit= lim)
                urls = self.client.get_messages(c, limit= lim, filter=InputMessagesFilterUrl)
                for u in urls:
                    if 'entities' in dir(u) and not u.entities is None:
                        for e in u.entities:
                            if 'url' in dir(e):
                                if not e.url in self.urls and not 'bot' in e.url:
                                    if not ' чп ' in u.text.lower() and not 'войн' in u.text.lower() and 'украин' not in u.text.lower():
                                        if abs(u.date.replace(tzinfo=None) - datetime.now()).total_seconds() / 3600 / 24 < 7:
                                            self.urls.append(e.url)
                                            self.urls_dict[e.url] = u.text
                                    else:
                                        #print('Skipped: {}'.format(u.text.lower()))
                                        pass
                    elif 'url' in dir(u):
                        self.urls.append(u.url)
                self.urls = list(dict.fromkeys(self.urls))
                #contacts = self.client.get_messages(c, limit= None, filter=InputMessagesFilterContacts)
                #for c in contacts:
                #    if 'contact' in dir(c):
                #        p = c.contact.phone_number
                mes_with_media = [x for x in mes if x.video != None]
                #for m in tqdm(mes_with_media, desc = c_name):
                downloaded_files = 0
                new_files_path = os.path.join('Output',sanitize_filepath(str(datetime.now().date())))
                if not os.path.exists(new_files_path):
                    os.makedirs(new_files_path)
                for m in mes_with_media:
                    try:
                        attr = m.video.attributes[0]
                        duration = attr.duration
                        if duration >= 4 * 60 and duration <= 6 * 60:
                            fname = m.file.name
                            ext = '.jpg'
                            if not fname is None and False:
                                ext = os.path.splitext(fname)[-1]
                            base_file_name = sanitize_filepath(str(m.date).replace(':','_'))
                            fname = "{}{}".format(base_file_name,ext)
                            if not os.path.exists(os.path.join(path,fname)):
                                t = m.download_media(thumb=-1, file=os.path.join(path,fname))
                                shutil.copyfile(os.path.join(path,fname), os.path.join(new_files_path, base_file_name + '_' + c_name.lower() + '_' + str(downloaded_files) + ext))
                                downloaded_files += 1
                        elif duration > 60 * 60:
                            postfix = '_long'
                            fname = m.file.name
                            ext = '.jpg'
                            if not fname is None and False:
                                ext = os.path.splitext(fname)[-1]
                            base_file_name = sanitize_filepath(str(m.date).replace(':','_'))
                            fname = "{}{}".format(base_file_name,ext)
                            if not os.path.exists(os.path.join(path + postfix,fname)):
                                if not os.path.exists(os.path.join(path + postfix)):
                                    os.makedirs(path + postfix)
                                if not os.path.exists(os.path.join(new_files_path + postfix)):
                                    os.makedirs(new_files_path + postfix)
                                t = m.download_media(thumb=-1, file=os.path.join(path + postfix, fname))
                                new_path = os.path.join(new_files_path + postfix, str(m.date).replace(':','_')[:7])
                                if not os.path.exists(new_path):
                                    os.makedirs(new_path)                                
                                shutil.copyfile(os.path.join(path + postfix,fname), os.path.join(new_path, base_file_name + '_' + c_name.lower() + '_' + str(downloaded_files) + ext))
                                downloaded_files += 1
                    except:
                        pass
                for m in mes:
                    m.mark_read()
                #print('Downloaded {} files'.format(downloaded_files))
                total_downloaded += downloaded_files
            except:
                pass
            # LOAD OLD AND STORE ONLY NEW
            if False or True:
                ids = [x.id for x in channels]
                with open('urls.txt','w', encoding="utf-8") as f:
                    self.urls = [x.replace('\n','') for x in self.urls if ('t.me/+' in x or 't.me/joinchat' in x) and 'bot' not in x.lower()]
                    #self.urls = [x for x in self.urls if 'join' in x]
                    for u in reversed(self.urls):
                        if u != '' and u != '\n':
                            '''
                            try:
                                id = CheckChatInviteRequest(u).hash.to_dict()['peer_id']['channel_id']
                                id = -1 * (id + 1001000000000)
                                if id in ids:
                                    continue
                            except:
                                continue
                            '''
                            if False and True and not u in sent_requests:
                                webbrowser.open(u, new=0, autoraise=True)
                                sent_requests.append(u)
                                with open('sent.txt','a') as f_sent:
                                    f_sent.write('{}\n'.format(u))
                                time.sleep(15)
                            f.write('{}\n'.format(u))
                with open('contacts.txt','w', encoding="utf-8") as f:
                    for c in self.contacts:
                        f.write('{}\n'.format(c))
                joinchats = [x for x in self.urls if 'join' in x]
            '''for u in joinchats:
                link = u.split('/')[-1]
                if not link in sent_requests:
                    result = ImportChatInviteRequest(link)
                    sent_requests.append(link)
            
                    time.sleep(1)'''
            self.EraseThumbnails(c_name.lower())
        print('Downloaded {} files'.format(total_downloaded))

class TestClient(TelegramClient):
    def __init__(self):
        self.api_id = '10966915'
        self.api_hash = '4b44f632cfdfc6171ed0456ad7b8497a'
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)
        self.client.connect()
        dialogs = self.client.iter_dialogs()
        groups = [x for x in dialogs if x.is_group]
        channels = [x for x in dialogs if x.is_channel]
        print("Total groups {}, total channels {}".format(len(groups), len(channels)))

start_time = datetime.now()
#client = TestClient()
client = MyClient()
end_time = datetime.now()
print('total runtime took {} sec'.format((end_time-start_time).total_seconds()))
