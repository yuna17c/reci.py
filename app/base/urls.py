from django.urls import path, include
from .views import FridgeHome, HomePage, RecipeFinderHome, DeleteView

urlpatterns = [
    path('', HomePage.as_view(), name='main'),
    path('fridge', FridgeHome.as_view(), name='fridge'),
    path('recipefinder', RecipeFinderHome.as_view(), name='recipe-finder'),
    path('ingredient-update/<int:pk>/', DeleteView.as_view(), name='ingredient-update'),
]
