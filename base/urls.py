from django.urls import path, include
from .views import *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', HomePage.as_view(), name='main'),
    path('pantry/', PantryHome.as_view(), name='pantry'),
    path('recipefinder/', RecipeFinderHome.as_view(), name='recipe-finder'),
    path('ingredient-update/<int:pk>/', DeleteView.as_view(), name='ingredient-update'),
    path('pantry-update/<int:pk>/', DeletePantryView.as_view(), name='pantry-update'),
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico')))
]