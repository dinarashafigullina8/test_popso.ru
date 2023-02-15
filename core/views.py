from django.shortcuts import render
from core.models import Post
from core.telegram_parser import main
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from core.config_api import *
import asyncio

# Сессия клиента telethon
session = '1ApWapzMBu6IIR5YIIj3ZLHHtljx-BZKbkzIII2VSiyGjauAZFJkM4KLV9sZxoKFbPj_kTk_6Pomb3vkw_eabBud8e7gR9z7y_DrZq6_ototLli3JJoY5cUUJg2nRDAmVgY7Aot1TC9LSRM6XWWb3eVYdPs-FDMYFuNq3Bqf6V6Qqzxi5ZTvYfK1CK0vSU_3zvE3LC6xIs1YFn0hvkwGZXH3Ao_xmkEW3pFo-g-76H56yjCJZzqMvdbkV8mJHRB_cVjCeadwARiqZ1juruUfrn4vv7EoS3Cm3LqCvbIT6ChJ71q2P9vyp2adCLKp4vwCQrsenfGy4qZ6hzU7aLaz6FddFZnjU1Js='


async def test():
    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        await client.connect()
        posts = await main(client)
        for post in posts:
            try:
                Post.objects.filter(tag=post['tag']).filter(post_id=post['post_id']).get()
            except:   
                new_post = Post(tag=post['tag'], date=post['date'], post_id=post['post_id'], photo=post['photo'], content=post['text'])
                new_post.save()
        # print(posts)
        # print(client.session.save())
        await client.run_until_disconnected()


def show_posts(self):
    
    asyncio.run(test())
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # async_result = loop.run_until_complete(test())
    # loop.close()
    # t = 5
    # # t = await main()
    # print(t)
    # for post in posts:
    #     print(post)
# with client:
#     client.loop.run_until_complete(show_posts())

def foo(request):
    return render(request, '/home/dinara/test_popso.ru/core/templates/admin.html')