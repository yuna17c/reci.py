from bs4 import BeautifulSoup
import aiohttp
import asyncio  
from .models import RecipeList, RecipeGenerator
from .extractinfo import *
import requests
import random
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def inputSearch(lst, mode):
    search = "https://www.allrecipes.com/search/results/?IngIncl="
    if (len(lst) == 1):
        search += lst[0]
    elif (len(lst) > 1):
        for ingredient in lst:
            search += "&IncIncl=" + ingredient
    
    if (mode == "many"):
        findRecipeNames(search)
    elif (mode == "one"):
        generate(search)

def generate(link):
    logging.warning('hi')
    recipeLinkList = []
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    all_results = soup.find_all('div', class_='component')
    recipe = random.choice(all_results)

    soupV2 = BeautifulSoup(recipe, 'lxml')
    recipeName = soupV2.find('h3', class_='card__title').get_text().strip()
    part = soup.find('a', {"class": 'card__titleLink'}, href=True)
    recipeLink = part['href']
    RecipeGenerator.objects.create(recipe_name = recipeName, link = recipeLink).save()
    recipeLinkList.append(part.get('href'))
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_details(recipeLinkList, "one"))    

def findRecipeNames(link):
    recipeNameList = []
    recipeLinkList = []
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    for parts in soup.find_all('h3', class_='card__title'):
        recipeName = parts.get_text().strip()
        recipeNameList.append(recipeName)
    i=0
    for part in soup.find_all('a', {"class":'card__titleLink'}, href=True):
        parent_tag = part.find_parent('div')['class']
        if parent_tag==['card__detailsContainer-left']:
            RecipeList.objects.create(recipe_name=recipeNameList[i], link=part['href']).save()
            elems = part.get('href')
            recipeLinkList.append(elems)
            i+=1
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_details(recipeLinkList, "many"))

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            text = await response.text()
            ingredients = await extract_ingredients(text)
            img_link = await extract_img_link(text)
            prep_time, minute = await extract_prep_time(text)
            return text, url, ingredients, img_link, prep_time, minute
    except Exception as e:
        print(str(e))


async def get_details(urls, mode):
    tasks=[]
    all_data=[]
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        all_data.extend(htmls)

        for html in htmls:
            if html is not None:
                if (mode == "many"):
                    recipeObject = RecipeList.objects.get(link=html[1])
                    recipeObject.prep_time = html[4]
                    recipeObject.prep_min = html[5]
                    recipeObject.img_link = html[3]
                    recipeObject.ingredients = html[2]
                    recipeObject.save()
                elif (mode == "one"):
                    recipeObject = RecipeGenerator.objects.get(link=html[1])
                    recipeObject.prep_time = html[4]
                    recipeObject.prep_min = html[5]
                    recipeObject.img_link = html[3]
                    recipeObject.ingredients = html[2]
                    recipeObject.save()

