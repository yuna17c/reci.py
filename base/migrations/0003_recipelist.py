# Generated by Django 3.2.3 on 2022-01-20 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_ingredient_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.TextField(blank=True, null=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('prep_time', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
