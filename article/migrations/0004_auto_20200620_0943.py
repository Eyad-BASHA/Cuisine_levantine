# Generated by Django 3.0.5 on 2020-06-20 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200620_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profiles/default_user.jpg', null=True, upload_to='profiles'),
        ),
    ]
