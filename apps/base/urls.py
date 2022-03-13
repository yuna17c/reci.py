from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', HomePage.as_view(), name='main'),
    path('pantry/', PantryHome.as_view(), name='pantry'),
    path('recipefinder/', RecipeFinderHome.as_view(), name='recipe-finder'),
    path('ingredient-update/<int:pk>/', DeleteView.as_view(), name='ingredient-update'),
    path('pantry-update/<int:pk>/', DeletePantryView.as_view(), name='pantry-update'),
    path('__debug__/', include('debug_toolbar.urls'))
]