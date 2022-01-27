from django.db import models
from django.utils import timezone
from datetime import date, timedelta

FOOD_GROUPS = (
    ("fruits", "fruits (e.g. apples, bananas)"),
    ("vegetables", "vegetables (e.g. broccoli, carrots)"),
    ("grains", "grains(e.g. bread, rice, pasta)"),
    ("protein", "protein (e.g. seafood, meat, eggs, nuts)"),
    ("dairy", "dairy (e.g. milk, cheese, non-dairy alternatives)"),
    ("cooking product", "cooking products (e.g. flour, cooking oil)"),
    ("herbs/spices", "herbs + spices (e.g. sugar, salt, paprika)"),
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

    @property
    def is_expired(self):
        return self.expiry_date <= date.today()
    
    @property
    def is_expiring_soon(self):
        return self.expiry_date <= date.today() + timedelta(days=5)

    def __str__(self):
        return self.name

class RecipeList(models.Model):
    recipe_name = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    prep_time = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.recipe_name

 