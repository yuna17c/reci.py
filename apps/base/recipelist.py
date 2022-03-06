from gettext import find
from bs4 import BeautifulSoup
import aiohttp
import asyncio  
from .changeToMin import changeToMinute
from .shorten import replaceUnits
from .models import RecipeList, RecipeGenerator
import requests

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

#not done :3
def generate(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    

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
    asyncio.run(get_details(recipeLinkList))

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

async def extract_ingredients(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        ings = soup.find_all('li', class_="ingredients-item")
        ing_text=""
        for i in ings:
            ing = i.get_text()
            ing=replaceUnits(ing)
            ing_text+=ing.replace(",", "")
            ing_text += ", "
        return ing_text
    except Exception as e:
        print(str(e))

async def extract_img_link(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        #print("*new*")
        if soup.find('div', class_="image-container") is not None:
            image = soup.find('div', class_="image-container").find("img")
            img_link = image.attrs['src']
            print("--" , str(img_link))
        elif soup.find('div', class_="image-slide") is not None:
            if soup.find_all('div', class_="image-slide")[1]:
                image = soup.find_all('div', class_="image-slide")[1].find("img")
                img_link = image.attrs['src']
        else:
            img_link = "../static/images/default.png"
        if img_link=="/img/icons/recipe-add-photo.jpg":
            img_link ="../static/images/default.png"
        return img_link
    except Exception as e:
        img_link = "../static/images/default.png"
        print(str(e))
        return img_link

async def extract_prep_time(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        minute=0
        total_time=""
        if soup.find("div", class_='recipe-meta-item-header', string="total:"):
            total = soup.find_all("div", class_='recipe-meta-item-header', string="total:")
            child = total[0].find_next_sibling("div")
            if child is not None:
                total_time = child.get_text()
                minute = changeToMinute(total_time)
        return total_time, minute
    except Exception as e:
        print(str(e))
        return "", 0

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
                recipeObject = RecipeList.objects.get(link=html[1])
                recipeObject.prep_time = html[4]
                recipeObject.prep_min = html[5]
                recipeObject.img_link = html[3]
                recipeObject.ingredients = html[2]
                recipeObject.save()

