from core.config_api import *
from core.models import Post
from telethon.sync import TelegramClient
from bs4 import BeautifulSoup
import requests



# Канал источник новостей @prime1
channel_source = ['https://t.me/market_marketplace', 'https://t.me/ozonmarketplace']

# Сессия клиента telethon
session = 'dinara'

client = TelegramClient(session, api_id, api_hash).start()

async def main():
    res = []
    for channel in channel_source:
        messages = await client.get_messages(channel, 1)
        tags = ['yandex', 'ozon']
        for post in messages:
            message_sql = {}
            if channel == 'https://t.me/market_marketplace':
                message_sql['tag'] = tags[0]
            else:
                message_sql['tag'] = tags[1]
            message_sql['date'] = post.date
            message_sql['text'] = post.text
            response = requests.get(channel+'/'+str(post.id)+'?embed=1&mode=tme')
            soup = BeautifulSoup(response.text, 'lxml')
            link_tag = str(soup.find('a', class_='tgme_widget_message_photo_wrap'))
            background_image = link_tag.split('background-image:url(')
            if background_image[0] == 'None':
                message_sql['photo'] = background_image[0]
            else:
                end_index = background_image[1].find('\')\"')
                message_sql['photo'] = background_image[1][1:end_index]
            print(message_sql)
            if message_sql['text'] != '':
                res.append(message_sql)
            

    
with client:
    client.loop.run_until_complete(main())

