from msilib.schema import ListView
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from bs4 import BeautifulSoup
import requests
from .models import Ingredient

class HomePage(ListView):
    model = Ingredient
    template_name = "base/home.html"

class RecipeFinderHome(ListView):
    model = Ingredient
    template_name = "base/recipe_home.html"
    def get_context_data(self, **kwargs):
        all_entries = Ingredient.objects.all()
        context = {'ingredients' : all_entries}
        return context
    def post(self, request):
        if 'add_button' in request.POST:
            user_input = request.POST.get("input", "")
            print(user_input)
            Ingredient.objects.create(name=user_input).save()
            all_entries = Ingredient.objects.all()
            context = {'ingredients' : all_entries}            
        elif 'done_button' in request.POST:
            all_entries = Ingredient.objects.all()
            context = {'ingredients' : all_entries} 
            input_list=[]
            for a in all_entries:
                print(a.name)
                input_list.append(a.name)
            inputSearch(input_list)
        return render(request, "base/recipe_home.html", context)


class DeleteView(DeleteView):
    model = Ingredient
    context_object_name = 'ingredient'
    success_url = reverse_lazy('recipe-finder')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class FridgeHome(ListView):
    model = Ingredient
    template_name = "base/fridge_home.html"


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
        recipeName = parts.get_text()
        recipeNameList.append(recipeName.strip())
    
    printRecipeNames(recipeNameList)

def printRecipeNames(lst):
    print("These are the possible recipes with your ingredients:")
    for item in lst:
        print("\t"+item)
