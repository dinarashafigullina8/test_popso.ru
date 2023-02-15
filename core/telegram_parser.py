import datetime

from core.models import Post
from telethon.sync import TelegramClient
from bs4 import BeautifulSoup
import requests



# Канал источник новостей @prime1
channel_source = ['https://t.me/market_marketplace', 'https://t.me/ozonmarketplace']



async def main(client:TelegramClient):
    # client.start()
    # client.run_until_disconnected()
    res = []
    for channel in channel_source:
        messages = await client.get_messages(channel, 10)
        tags = ['yandex', 'ozon']
        for post in messages:
            message_sql = {}
            if channel == 'https://t.me/market_marketplace':
                # a = Post(tag=tags[0], date= datetime.now().time(), content='None')
                # a.save()
                message_sql['tag'] = tags[0]
            else:
                # a = Post(tag=tags[1], date= datetime.now().time(), content='None')
                # a.save()
                message_sql['tag'] = tags[1]
            
            # a.date = post.date
            # a.content = post.text
            message_sql['date'] = post.date
            message_sql['text'] = post.text
            message_sql['post_id'] = post.id
            response = requests.get(channel+'/'+str(post.id)+'?embed=1&mode=tme')
            soup = BeautifulSoup(response.text, 'lxml')
            link_tag = str(soup.find('a', class_='tgme_widget_message_photo_wrap'))
            background_image = link_tag.split('background-image:url(')
            if background_image[0] == 'None':
                message_sql['photo'] = background_image[0]
            else:
                end_index = background_image[1].find('\')\"')
                message_sql['photo'] = background_image[1][1:end_index]
            if message_sql['text'] != '':
                res.append(message_sql)
    return res


 



