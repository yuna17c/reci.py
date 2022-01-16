from django.urls import path, include
from .views import FridgeHome, HomePage, RecipeFinderHome

urlpatterns = [
    path('', HomePage.as_view(), name='main'),
    path('fridge', FridgeHome.as_view(), name='fridge'),
    path('recipefinder', RecipeFinderHome.as_view(), name='recipe-finder'),
]
