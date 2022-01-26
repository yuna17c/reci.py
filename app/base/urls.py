from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='main'),
    path('fridge/', FridgeHome.as_view(), name='fridge'),
    path('fridge/group1/', FridgeHome.as_view(), name='test1'),
    path('fridge/group2/', FridgeHome.as_view(), name='test2'),
    path('recipefinder/', RecipeFinderHome.as_view(), name='recipe-finder'),
    path('ingredient-update/<int:pk>/', DeleteView.as_view(), name='ingredient-update'),
    path('fridge-update/<int:pk>/', DeleteFridgeView.as_view(), name='fridge-update')
]
