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
from .models import *
import random
import aiohttp
import asyncio  
from .changeToMin import changeToMinute
from .shorten import replaceUnits

class HomePage(TemplateView):
    model = FoodItem
    template_name = "base/home.html"
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        recipes = list(RecipeGenerator.objects.all())
        context['ingredients'] = FoodItem.objects.all()
        context['recipe'] = random.choice(recipes)
        return context
    def post(self, request, *args, **kwargs):
        if 'generate' in request.POST:
            RecipeGenerator.objects.all().delete()
            all_ingredients = FoodItem.objects.all()
            ingredients = []
            for i in all_ingredients:
                ingredients.append(i.name)
            random_num = random.randint(1, len(ingredients))
            input_list = random.choices(ingredients, k=random_num)
            inputSearch(input_list, 1)
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context=context)
            
        return HttpResponseRedirect(request.path_info)
    
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
            inputSearch(input_list, 0)
        elif 'desc_button' in request.POST:
            # compare = request.POST.get("compare", "")
            # amount = request.POST.get("amount", "")
            print("yes")
            recipe = RecipeList.objects.all().order_by('prep_min')
        elif 'asc_button' in request.POST:
            print("asc")
        return HttpResponseRedirect(request.path_info)

class DeleteView(DeleteView):
    model = Ingredient
    context_object_name = 'ingredient'
    success_url = reverse_lazy('recipe-finder')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class DeletePantryView(DeleteView):
    model = FoodItem
    context_object_name = 'item'
    success_url = reverse_lazy('pantry')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class PantryHome(TemplateView):
    model = FoodItem
    template_name = "base/pantry_home.html"
    def get_context_data(self, **kwargs):
        context = super(PantryHome, self).get_context_data(**kwargs)
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

def inputSearch(lst, mode):
    search = "https://www.allrecipes.com/search/results/?IngIncl="
    if (len(lst) == 1):
        search += lst[0]
    elif (len(lst) > 1):
        for ingredient in lst:
            search += "&IncIncl=" + ingredient
    
    #webbrowser.open(search)
    findRecipeNames(search, mode)

def findRecipeNames(link, mode):
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
            if (mode==0):
                RecipeList.objects.create(recipe_name=recipeNameList[i], link=part['href']).save()
            elif(mode==1):
                RecipeGenerator.objects.create(name=recipeNameList[i], link=part['href']).save()
            elems = part.get('href')
            recipeLinkList.append(elems)
            i+=1

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_details(recipeLinkList, mode))

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
        if soup.find('div', class_="image-container") is not None:
            image = soup.find('div', class_="image-container").find("img")
            img_link = image.attrs['src']
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
                if (mode==0):
                    recipeObject = RecipeList.objects.get(link=html[1])
                    recipeObject.prep_time = html[4]
                    recipeObject.prep_min = html[5]
                    recipeObject.img_link = html[3]
                    recipeObject.ingredients = html[2]
                    recipeObject.save()

                elif (mode==1):
                    recipeObject = RecipeGenerator.objects.get(link=html[1])
                    recipeObject.prep_time = html[4]
                    recipeObject.prep_min = html[5]
                    recipeObject.img_link = html[3]
                    recipeObject.ingredients = html[2]
                    recipeObject.save()

