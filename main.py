"""
    1. Register app instance on my.telegram.org and fill APP_API_ID (int) and APP_API_HASH (str) vars
    2. Place channels.csv and keywords.csv on the same level as this script.
        Fill first row in files with keywords you want and delimit them with ','
    3. Place requirements.txt on the same level
    4. Run pip install -r requirements.txt
    5. Run this script with python3 <sript-name>.py or IDE
    6. Provide phone number
    7. Pass received code
    8. Processing... (after finding all messages you will be provided with y/n statement for each chat in your telegram)
    9. To run someone else telegram delete session file in root folder after finishing cleaning previous account
    10. Make sure to delete everything related to this script after processing
    11. Delete CPython session in telegram active sessions
"""

import asyncio
from collections import defaultdict
from tqdm import tqdm
from typing import DefaultDict, Dict

from pyrogram import Client

# TODO Provide this info from my.telegram.org
APP_API_ID: int = 10000000
APP_API_HASH: str = "jd293dju483f1c3634636a8db5aaaiwd93"

TYPES = {'group', 'private'}


class ChatsToDelete:
    id: int
    name: str

    def __init__(self):
        self.msgs: Dict[int, str] = dict()


class MessagesToDelete:
    def __init__(self):
        self.chats: DefaultDict[int, ChatsToDelete] = defaultdict(lambda: ChatsToDelete())


async def fetch_vulnerable_messages(app, keywords) -> MessagesToDelete:
    chat_msgs = MessagesToDelete()

    for keyword in tqdm(keywords):
        search = app.search_global(keyword)
        if not search:
            continue

        async for message in app.search_global(keyword):
            if message.chat.type not in TYPES:
                continue

            text = ''

            if message.forward_signature or message.forward_sender_name or message.forward_from_chat:
                text = '#forward '
                if message.forward_signature:
                    text += message.forward_signature + ' '
                if message.forward_sender_name:
                    text += message.forward_sender_name + ' '
                if message.forward_from_chat and message.forward_from_chat.title:
                    text += message.forward_from_chat.title + ' '

            if message.media and message.web_page is None:
                text += str(message.caption or '')
            else:
                text += str(message.text or '')

            if message.web_page:
                text += f' #webpage: {message.web_page.title}//{message.web_page.description}//{message.text}'

            if text == 'None':
                print()

            msg_chat = message.chat

            chat_id = msg_chat.id
            chat_msgs.chats[chat_id].id = chat_id

            if msg_chat.type == 'private':
                name = f'{msg_chat.first_name} {msg_chat.last_name}' if msg_chat.first_name else msg_chat.username
            else:
                name = msg_chat.title

            chat_msgs.chats[chat_id].name = str(name)

            if message.message_id not in chat_msgs.chats[chat_id].msgs:
                chat_msgs.chats[chat_id].msgs[message.message_id] = text

    return chat_msgs


async def clean_telegram(keywords):
    async with Client("my_account", APP_API_ID, APP_API_HASH) as app:
        chat_msgs = await fetch_vulnerable_messages(app, keywords)
        print(chat_msgs.chats.values())
        for chat_msg in chat_msgs.chats.values():
            print('\n\n' + chat_msg.name)
            for msg_text in chat_msg.msgs.values():
                text = msg_text.replace('\n', ' ') if msg_text else msg_text
                print(f'\t{text}')

            print(f'Delete messages from {chat_msg.name}? (y/n)')
            while True:
                char = input()

                if char.lower() not in ['y', 'n']:
                    print('Try again.')
                    continue

                if char.lower() == 'y':
                    for i, msg_ids in enumerate(tqdm(list(chat_msg.msgs.keys()))):
                        if i % 100 == 0:
                            # Sleep to prevent throttling
                            await asyncio.sleep(1)
                        await app.delete_messages(chat_msg.id, msg_ids)

                    print(f'Messages from {chat_msg.name} deleted.')
                else:
                    print('Skipped.')
                break


if __name__ == '__main__':
    with open('keywords.csv') as file:
        keywords = file.readline().split(',')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(clean_telegram(keywords))
