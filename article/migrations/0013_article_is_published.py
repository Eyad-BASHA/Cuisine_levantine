# Generated by Django 3.0.7 on 2020-06-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20200628_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]