# Generated by Django 3.0.7 on 2020-07-03 13:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0014_auto_20200702_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_likes',
            field=models.ManyToManyField(related_name='reply_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
