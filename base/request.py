import requests
import re
import json
from .models import RecipeList, RecipeGenerator

# api_url = "https://recipeland.com/recipes/ingredients/search"
api_url = "https://d1.supercook.com/dyn/results"
dat = {}
title_lst = []

def create_payload(ing_lst):
    joined = ",".join(ing_lst)
    print("joined",joined)
    payload = {
        'needsimage': '1',
        'app': '1',
        'kitchen': joined,
        'focus': '',
        'exclude': '',
        'kw': '',
        'catname': '',
        'start': '0',
        'fave': 'false',
        'lang': 'en',
        'cv': '2'
    }
    response = requests.post(api_url, data=payload)
    name_lst = find_name(response.text)
    print(name_lst)


def find_name(resp):
    data = json.loads(resp)
    rl_name = [recipe['title'] for recipe in data['results']]
    rl_img = [recipe['img'] for recipe in data['results']]
    lst = []
    for i,name in enumerate(rl_name):
        link = ""
        img_link = rl_img[i]
        RecipeList.objects.create(recipe_name=name, link=link, img_link=img_link).save()

    return lst
