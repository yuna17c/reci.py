import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from asgiref.sync import async_to_sync, sync_to_async

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            # 1. Extracting the Text:
            text = await response.text()
            # 2. Extracting the  Tag:
            title_tag = await extract_title_tag(text)
            return text, url, title_tag
    except Exception as e:
        print(str(e))

async def extract_title_tag(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        return soup.title
    except Exception as e:
        print(str(e))

async def get_details(urls):
    tasks=[]
    all_data=[]
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        all_data.extend(htmls)
        for html in htmls:
            if html is not None:
                print(html[1])
                print(html[2])
                print("----YO----")

# get_details(['http://google.com', 'http://instagram.com', 'http://facebook.com'])
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(get_details(['http://tim.blog', 'http://google.com', 'http://instagram.com']))
#async_to_sync(get_details(['http://tim.blog', 'http://google.com', 'http://instagram.com']))
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(get_details(['http://tim.blog', 'http://google.com', 'http://instagram.com']))
# except:
#     pass