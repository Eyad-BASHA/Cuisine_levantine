# Generated by Django 3.0.7 on 2020-07-06 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0019_auto_20200705_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_comment',
            field=models.BooleanField(default=True),
        ),
    ]
