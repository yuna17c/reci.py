
from .changeToMin import changeToMinute
from .shorten import replaceUnits
from gettext import find
from bs4 import BeautifulSoup
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    logger.warning("image")
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