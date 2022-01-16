from msilib.schema import ListView
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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
        user_input = request.POST.get("input", "")
        print(user_input)
        Ingredient.objects.create(name=user_input).save()
        all_entries = Ingredient.objects.all()
        context = {'ingredients' : all_entries}
        for a in all_entries:
            print(a.name)
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