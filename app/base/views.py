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

class HomePage(ListView):
    model = Ingredient
    template_name = "base/home.html"

class RecipeFinderHome(TemplateView):
    template_name = "base/recipe_home.html"
    #context_object_name = 'recipe-finder'
    #queryset = Ingredient.objects.all()
    def get_context_data(self, **kwargs):
        # all_ingredients = Ingredient.objects.all()
        # all_recipes = RecipeList.objects.all()
        # context = super(RecipeFinderHome, self).get_context_data(**kwargs)
        # context['1'] = {'ingredients' : all_ingredients}
        # context['2'] = {'recipes' : all_recipes}
        context = super(RecipeFinderHome, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        context['recipe_list'] = RecipeList.objects.all()
        return context
    def post(self, request):
        if 'add_button' in request.POST:
            user_input = request.POST.get("input", "")
            print(user_input)
            Ingredient.objects.create(name=user_input).save()
            # all_entries = Ingredient.objects.all()
            # for a in all_entries:
            #     print(a.name)
            # all_entries = Ingredient.objects.all()
            #context['ingredients'] = {'ingredients' : all_entries}   
            #context['ingredients'] = Ingredient.objects.all()
        elif 'done_button' in request.POST:
            RecipeList.objects.all().delete()
            all_entries = Ingredient.objects.all()
            #context['ingredients'] = Ingredient.objects.all()
            input_list=[]
            for a in all_entries:
                print(a.name)
                input_list.append(a.name)
            inputSearch(input_list)
        #return render(request, "base/recipe_home.html")
        #return self.get_response(request)
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
            FoodItem.objects.create(name=name, expiry_date=expiry_date).save()
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
            i+=1
    printRecipeNames(recipeNameList)

def printRecipeNames(lst):
    if len(lst)==0:
        print("There are no possible recipes that match your ingredients.")
    else:
        print("These are the possible recipes with your ingredients:")
    for item in lst:
        print("\t"+item)
