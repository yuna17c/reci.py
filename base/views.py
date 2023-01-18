from contextlib import nullcontext
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from .models import *
import random
from .recipelist import *
from django.shortcuts import redirect, render
from .request import *
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, "home.html")

class HomePage(TemplateView):
    model = FoodItem
    template_name = "base/index.html"    
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['ingredients'] = FoodItem.objects.all()
        context['recipe'] = RecipeGenerator.objects.first()
        return context
    def post(self, request):
        if 'close' in request.POST:
            logger.warning("generating")
            RecipeGenerator.objects.all().delete()
            all_ingredients = FoodItem.objects.all()
            ingredients = []
            for i in all_ingredients:
                ingredients.append(i.name)
            random_num = random.randint(1, len(ingredients))
            input_list = random.sample(ingredients, k=random_num)
            inputSearch(input_list, "one")
            create_payload(input_list)
            
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
            print("---added: ", user_input)
            Ingredient.objects.create(name=user_input).save()
        elif 'done_button' in request.POST:
            RecipeList.objects.all().delete()
            all_entries = Ingredient.objects.all()
            input_list=[]
            for a in all_entries:
                print("---ing: ", a.name)
                input_list.append(a.name)
            inputSearch(input_list, "many")
            create_payload(input_list)
        elif 'desc_button' in request.POST:
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

class DeletePantryView(DeleteView):
    model = FoodItem
    context_object_name = 'item'
    success_url = reverse_lazy('pantry')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)