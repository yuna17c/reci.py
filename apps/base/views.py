from contextlib import nullcontext
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from .models import *
import random
from .recipelist import *
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class HomePage(TemplateView):
    model = FoodItem
    template_name = "base/home.html"    
    logger.warning('hello')
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['ingredients'] = FoodItem.objects.all()
        recipes = RecipeGenerator.objects.all()
        if (recipes):
            context['recipe'] = random.choice(recipes)
        else:
            context['recipe'] = nullcontext
        return context
    def post(self, request, *args, **kwargs):
        if 'generate' in request.POST:
            RecipeGenerator.objects.all().delete()
            all_ingredients = FoodItem.objects.all()
            ingredients = []
            for i in all_ingredients:
                ingredients.append(i.name)
            random_num = random.randint(1, len(ingredients))
            input_list = random.sample(ingredients, k=random_num)

            #generate(input_list)
            
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
            inputSearch(input_list, "many")
        elif 'desc_button' in request.POST:
            # compare = request.POST.get("compare", "")
            # amount = request.POST.get("amount", "")
            print("yes")
            recipe = RecipeList.objects.all().order_by('prep_min')
            # for i in recipe:
            #     recipeObject = RecipeList.objects.get(recipe_name=i)


            # all_entries = RecipeList.objects.all()
            # for a in all_entries:
            #     print(a.recipe_name, a.prep_min)
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
