# Generated by Django 3.0.5 on 2020-06-20 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_user.jpg', null=True, upload_to='media/profiles'),
        ),
    ]
