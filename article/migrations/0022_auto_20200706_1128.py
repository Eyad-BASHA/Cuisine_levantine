# Generated by Django 3.0.7 on 2020-07-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0021_auto_20200706_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_comment',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]