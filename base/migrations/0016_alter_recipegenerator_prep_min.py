# Generated by Django 3.2.6 on 2022-02-28 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20220228_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipegenerator',
            name='prep_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
