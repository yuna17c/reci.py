from ast import Try
from unicodedata import name
from django import forms
from msilib.schema import ListView
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from bs4 import BeautifulSoup
import requests
from .models import Ingredient, FoodItem, RecipeList
import random
import aiohttp
import asyncio
from asgiref.sync import async_to_sync, sync_to_async


def all_food_items(request):
    food_list = FoodItem.objects.all()
    return render(request, 'base/home.html', 
    { 'food_list' : food_list })

def modal_view(request):
    text = "test"
    return render(request, "base/recipe_generator.html", locals())

class HomePage(ListView):
    model = Ingredient
    template_name = "base/home.html"
    
class RecipeFinderHome(TemplateView):
    template_name = "base/recipe_home.html"
    def get_context_data(self, **kwargs):
        context = super(RecipeFinderHome, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        context['recipe_list'] = RecipeList.objects.all()
        return context
    def post(self, request):
        if 'add_button' in request.POST:
            user_input = request.POST.get("input", "")
            print(user_input)
            Ingredient.objects.create(name=user_input).save()
        elif 'done_button' in request.POST:
            RecipeList.objects.all().delete()
            all_entries = Ingredient.objects.all()
            input_list=[]
            for a in all_entries:
                print(a.name)
                input_list.append(a.name)
            inputSearch(input_list)
        return HttpResponseRedirect(request.path_info)

class DeleteView(DeleteView):
    model = Ingredient
    context_object_name = 'ingredient'
    success_url = reverse_lazy('recipe-finder')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class DeleteFridgeView(DeleteView):
    model = FoodItem
    context_object_name = 'item'
    success_url = reverse_lazy('fridge')

class FridgeHome(TemplateView):
    model = FoodItem
    template_name = "base/fridge_home.html"
    def get_context_data(self, **kwargs):
        context = super(FridgeHome, self).get_context_data(**kwargs)
        context['food_items'] = FoodItem.objects.all()
        return context
    def post(self, request):
        if 'add_button' in request.POST:
            name = request.POST.get("name", "")
            expiry_date = request.POST.get("expiry", "")
            food_group = request.POST.get("food_group", "")
            FoodItem.objects.create(name=name, expiry_date=expiry_date, food_group=food_group).save()
        
        all_items = FoodItem.objects.all()
        names = []
        for item in all_items:
            names.append(item.name)
        request.session['food_names'] = names
        return HttpResponseRedirect(request.path_info)


class RecipeGenerator(TemplateView):
    model = FoodItem
    template_name = "base/home.html"
    def post(self, request):
        FridgeHome.post(self, request)
        ingredients = request.session['food_names']
        #inputSearch(ingredients)
        return HttpResponseRedirect(request.path_info)

def inputSearch(lst):
    search = "https://www.allrecipes.com/search/results/?IngIncl="
    if (len(lst) == 1):
        search += lst[0]
    elif (len(lst) > 1):
        for ingredient in lst:
            search += "&IncIncl=" + ingredient
    
    #webbrowser.open(search)
    findRecipeNames(search)

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
            prep_time = await extract_prep_time(text)
            return text, url, ingredients, img_link, prep_time
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
        if soup.find('div', class_="image-container") is not None:
            image = soup.find('div', class_="image-container").find("img")
            img_link = image.attrs['src']
        else: 
            img_link = "../static/images/default.png"
        if img_link=="/img/icons/recipe-add-photo.jpg":
            img_link="../static/images/default.png"
        return img_link
    except Exception as e:
        print(str(e))

async def extract_prep_time(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        titles = soup.find('div', class_='two-subcol-content-wrapper')
        child = titles.select_one(":nth-child(3)")
        if child is not None:
            total_time = child.get_text().strip()[7:]
            #minuteTime = changeToMinute(total_time)
        else: 
            total_time=""
        return total_time
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
                recipeObject = RecipeList.objects.get(link=html[1])
                recipeObject.prep_time = html[4]
                recipeObject.img_link = html[3]
                recipeObject.ingredients = html[2]
                recipeObject.save()

def replaceUnits(text):
    text=text.replace("tablespoons", "tbsp")
    text=text.replace("tablespoon", "tbsp")
    text=text.replace("teaspoons", "tsp")
    text=text.replace("teaspoon", "tsp")
    text=text.replace("pounds", "lbs")
    text=text.replace("pound", "lb")
    text=text.replace("ounce", "oz")
    lst = ["or to taste", "to taste", "lengthwise", "diced", "chopped", "minced", "cooked", "beaten", "peeled"]
    find_next=False
    for i in lst:
        words = text.split(" ")
        for word in words:
            if find_next:
                if word=="and":
                    text=text.replace(word, "")
                find_next=False
            if word==i:   
                find_next=True
        text=text.replace(i , "")
    return text

def printRecipeNames(lst):
    if len(lst)==0:
        print("There are no possible recipes that match your ingredients.")
    else:
        print("These are the possible recipes with your ingredients:")
    for item in lst:
        print("\t"+item)


def changeToMinute(str):
    x = str.split("hr")
    hour = 0
    min = 0
    if len(x) > 1:
        hour = x[0].strip()
    min_idx = x[-1].find("min")
    if min_idx!=-1:
        min = x[-1][:min_idx].strip()
        if min[0].isnumeric()==False:
            min = min[2:]
    total=60*int(hour)+int(min)
    return total


