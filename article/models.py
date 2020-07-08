from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.forms.models import modelformset_factory
from PIL import Image
from ckeditor.fields import RichTextField






# ==================== User Profile ========================
# def upload_profile_path(instance, filename):
#     return '/'.join(['profiles', str(instance.user), filename])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles', default='profiles/default_user.jpg', null=True, blank=True)
    is_comment = models.BooleanField(default=True)


    def __str__(self):
        # return self.user.username
        # return f'{self.user.username} Profile'
        return '%s %s' %(self.user.username, self.is_comment)

    def save(self, force_insert=False,force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()






# ================ Category & Article ==========================
class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True, default=None)

    def  __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name






class Article(models.Model):

    LANGUAGES = [
        ('AR', 'عربي'),
        ('FR', 'Française'),
        ('EN', 'English'), 
    ]

    language = models.CharField(max_length=20, choices=LANGUAGES, default='ar')

    # auther = models.ForeignKey(User, settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True )
    auther = models.ForeignKey(User, null=True, related_name="article_auther", on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name='cat', on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, related_name='sub_category', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    
    description = RichTextField(max_length=5000, blank=False, null=False)
    # description = models.TextField(max_length=2500, blank=False, null=False)
    date_published = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    date_updated = models.DateTimeField(blank=True, null=True, default=None)
    is_published = models.BooleanField(default=False)

    likes = models.ManyToManyField(User, related_name='likes')

    favorites = models.ManyToManyField(User, related_name='favorites')


    class Meta:
        ordering = ['-id']


    def __str__(self):
        return self.title
        # return '%s %s %s %s %s' % (self.category, self.sub_category, self.title, self.auther.username, self.description)

    def total_likes(self):
        return self.likes.count()  
    
    def user_like(self):
        return self.likes.users


    def total_favorites(self):
        return self.favorites.count()

    def get_absolute_url(self):
        return reverse("article:detail", args=[self.id])


def upload_path(instance, filename):
    return '/'.join(['covers', str(instance.article), filename])


class Medias(models.Model):
    auther = models.ForeignKey(User, null=True, related_name="media_auther", on_delete=models.SET_NULL)
    title = models.CharField(max_length=500, blank=True)
    media = models.FileField(upload_to=upload_path, blank=True, null=True)
    article = models.ForeignKey(Article, default=None, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    date_updated = models.DateTimeField(blank=True, null=True, default=None)
    
    # cover = models.FileField(upload_to=upload_path)

    # class Meta:
    #     ordering = ['title',]

    # def __unicode__(self):
    #     return self.title

    # def get_absolute_url(self):
    #     return reverse('home', kwargs={'article': self.article})



    def __str__(self):
        # return self.media
        return self.article.title + " Media"
        # return self.article.title
        # if self.article:
        #     return '%s (%s)' %(self.id, self.article.title)
        # return '%s - %s - %s - %s' % (self.article, self.article.category, self.article.sub_category, self.article.description, self.media)


# @receiver(pre_save, sender=Article)
# def pre_save_title(sender, **kwargs):
#     title = 


class Comment(models.Model): 
    auther = models.ForeignKey(User, null=True, related_name="user_comment", on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete=models.SET_NULL)
    comment_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    comment_likes = models.ManyToManyField(User, related_name='comment_likes')
    reply_likes = models.ManyToManyField(User, related_name='reply_likes')

    def __str__(self): 
        return '%s - %s' %(self.auther.username, self.article.title)

    def total_comment_likes(self):
        return self.comment_likes.count()

    def total_reply_likes(self):
        return self.reply_likes.count()

    def user_like(self):
        return self.comment_likes.user.username

