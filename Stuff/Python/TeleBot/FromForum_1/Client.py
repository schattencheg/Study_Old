from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogFiltersRequest
from telethon.tl.functions.messages import UpdateDialogFilterRequest
from telethon.tl.types import InputPeerUser
from telethon.tl.types import InputMessagesFilterVideo, InputMessagesFilterUrl

session_string = 'session_name'
api_id = 10966915
api_hash = '4b44f632cfdfc6171ed0456ad7b8497a'

async def get_folders():
    request = await client(GetDialogFiltersRequest())
    return dict(zip([x.title for x in request],request))

async def update(folder_id, new):
    request = await client(UpdateDialogFilterRequest(folder_id, new))
    print(request)

with TelegramClient(session_string, api_id, api_hash) as client:
    t = client.loop.run_until_complete(get_folders())['SHL'] # here i get DialogFilter
    selected_dialogs_ids = [y.to_dict()['channel_id'] for y in t.include_peers]
    dialogs = [x for x in client.get_dialogs()]
    dialogs_ids = [x.id for x in dialogs]
    needed = [x for x in dialogs if x.id in selected_dialogs_ids]

    for peer in t.include_peers:
        print(peer)
        messages = client.get_messages(peer, limit= None, filter=InputMessagesFilterVideo)
    entity = client.get_entity('Sposiboh')
    print(type(entity), entity)

    to_add = InputPeerUser(entity.id, entity.access_hash) # i get user entity and convert it to PeerUser
    
    t.include_peers.append(to_add) # i add to_add to the list of other users in DialogFilter
    client.loop.run_until_complete(update(162, t)) # 162 is folder id that i got from GetDialogFiltersRequest
    print('ok')