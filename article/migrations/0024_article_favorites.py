# Generated by Django 3.0.7 on 2020-07-07 19:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0023_auto_20200706_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
