import re
import json

from core.models import Post
from telethon.sync import TelegramClient
from bs4 import BeautifulSoup
import requests



# Канал источник новостей @prime1
channel_source = ['https://t.me/s/market_marketplace/', 'https://t.me/s/ozonmarketplace/']

def parser_telegram():
    
    for channel in channel_source:
        tags = ['yandex', 'ozon']
        if channel == 'https://t.me/s/market_marketplace/':
            type = tags[0]
        else:
            type = tags[1]
        response = requests.get(channel)
        soup = BeautifulSoup(response.text, 'lxml')
        data_post = soup.find('div', ['tgme_widget_message', 'text_not_supported_wrap', 'js-widget_message'])
        first_post_id = data_post.attrs['data-post'].split('/')[1]
        response1 = requests.get(channel+'?before='+first_post_id)
        soup1 = BeautifulSoup(response1.text, 'lxml')
        data_posts = list(soup1.find_all('div', ['tgme_widget_message', 'text_not_supported_wrap', 'js-widget_message']))
        
        for post in data_posts[:10]:
            post_id = post.attrs['data-post'].split('/')[1]
            imgs = list(post.find_all('a', 'tgme_widget_message_photo_wrap'))
            time = post.find('time', 'time').attrs['datetime']
            
            res_img = []
            for img in imgs:
                background_image = str(img).split('background-image:url(')
                if background_image[0] != 'None':
                    end_index = background_image[1].find('\')\"')
                    t = background_image[1][1:end_index]
                    res_img.append(t)
                    
            texts = list(post.find_all('div', ['tgme_widget_message_text',"js-message_text",'before_footer']))
            for text_with_tags in texts:
                text = re.sub(r'\<[^>]*\>', '', str(text_with_tags))
                
            d = {
                'tag': type,
                'img': res_img,
                'post_id': post_id,
                'time': time,
                'text': text,
            }
            if Post.objects.filter(tag=d['tag'], post_id=d['post_id']).exists():
                print('skip', d['post_id']) 
            else:   
                t = Post(tag=d['tag'],post_id=d['post_id'],date=d['time'],content=d['text'],photo=json.dumps(d['img']))
                t.save()
    return



