import django
from django.db import models
from django.utils import timezone

FOOD_GROUPS = (
    ("fruits", "fruits/vegetables"),
    ("fats", "fats + oils"),
    ("dairy", "eggs, milk and milk products"),
    ("meat", "meat + fish"),
    ("herbs", "herbs + spices"),
    ("grain", "grain, nuts and baking products"),
    ("pasta", "pasta, rice and pulses"),
    ("other", "other")
)
# Create your models here.
class Ingredient(models.Model):
    name = models.TextField(null=True, blank=True)
    # title = models.CharField(max_length=200)
    # complete = models.BooleanField(default=False)
    # created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.TextField(null=True, blank=False)
    expiry_date = models.DateField(null=True, blank=False)
    food_group = models.TextField(choices=FOOD_GROUPS, default="other")
    def __str__(self):
        return self.name

class RecipeList(models.Model):
    recipe_name = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    prep_time = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.recipe_name

 