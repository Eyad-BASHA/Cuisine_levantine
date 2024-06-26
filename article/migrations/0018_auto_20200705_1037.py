# Generated by Django 3.0.7 on 2020-07-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0017_remove_article_likes_heart'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='language',
            field=models.CharField(choices=[('AR', 'عربي'), ('FR', 'Française'), ('EN', 'English')], default='ar', max_length=20),
        ),
    ]
