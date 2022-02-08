from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='main'),
    path('fridge/', FridgeHome.as_view(), name='fridge'),
    path('recipefinder/', RecipeFinderHome.as_view(), name='recipe-finder'),
    path('#recipe_generator', RecipeGenerator.as_view(), name='recipe-generator'),
    path('ingredient-update/<int:pk>/', DeleteView.as_view(), name='ingredient-update'),
    path('fridge-update/<int:pk>/', DeleteFridgeView.as_view(), name='fridge-update')
]