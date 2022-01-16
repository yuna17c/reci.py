from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.TextField(null=True, blank=True)
    # title = models.CharField(max_length=200)
    # complete = models.BooleanField(default=False)
    # created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
        