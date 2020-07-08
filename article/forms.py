from django import forms
from django.forms import MultiWidget
from .models import *
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from upload_validator import FileTypeValidator
from django.utils.translation import gettext_lazy as _




# ============ User =============================
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label=_('Prénom'))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label=_('Nom'))
    email = forms.EmailField(max_length=254,  required=True, help_text='Required. Inform a valid email address.', label=_('Email'))                                                                                                                                                                                                        

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email', 
        ]

class ProfileUpdateForm(forms.ModelForm):
    profile_pic = forms.FileField(
        label=_('image'), help_text=_("Seuls les formats d’image sont acceptés"), required=False,
        validators=[FileTypeValidator(
            allowed_types=[ 'image/*']
        )]
    )

    class Meta:
        model = Profile
        fields = ['birth_date', 'profile_pic']
        labels = {
            'birth_date': _('Date de Naissance'),
            'profile_pic': _('Image de Profil'),
        }




class UserCommentForm(forms.ModelForm):
    # is_comment = forms.BooleanField(label="Active / Desactive la Commenter", required=False)
    class Meta:
        model = Profile
        fields = ['is_comment',]
        labels = {
            'is_comment': _('peuvent commenter'),
        }



class UserUpdateConfForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'is_superuser',
            'is_staff',
            'is_active',
        ]
        


# ============ Category & Article =============================
class CategoryForm(forms.ModelForm):
    name = forms.CharField(label="Catégorie")
    class Meta:
        model = Category
        fields = [
            'name', 
        ]

class SubCategoryForm(forms.ModelForm):
    name = forms.CharField(label="Sous-Category")
    class Meta:
        model = SubCategory
        fields = [
            'name', 
        ]







class MediaForm(forms.ModelForm):
    # file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    
    media = forms.FileField(
        label='media', help_text="image and video formats are accepted.", required=False,
        validators=[FileTypeValidator(
            allowed_types=[ 'image/*', 'video/*']
        )]
    )

    class Meta:

        model = Medias
        fields = [
            'media', 
        ]


        # attachments = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

        # If you need to upload media files, you can use this:
        # attachments = MultiMediaField(
        #     min_num=1,
        #     max_num=3,
        #     max_file_size=1024*1024*5,
        #     media_type='video',  # 'audio', 'video' or 'image'
        # )


         # For images (requires Pillow for validation):
        # attachments = MultiImageField(min_num=1, max_num=3, max_file_size=1024*1024*5)


        
        # .widget.attrs.update({
        #     'multiple'
        # })
        
        # widgets = {
        #     'media': (attrs={'multiple'})   
        # }

# class RawMediaForm(forms.Form):
#     media = forms.FileField(widget=forms.FileField(Label='Media', widget=forms.FileField(attrs={'multiple'}))

class ArticleForm(forms.ModelForm):
    # language = forms.CharField(label="Langue")
    # category = forms.CharField(label="Catégorie")
    # sub_category = forms.CharField(label="Sous Catégorie")
    # title = forms.CharField(label="Titre")
    # is_published = forms.BooleanField(label="est publié", required=False)

    class Meta:
        model = Article
        fields = [
            'language',
            'category', 
            'sub_category', 
            'title', 
            'description',
            'is_published',
        ]
        labels = {
            'language': _('Langue'),
            'category': _('Catégorie'),
            'sub_category': _('Sous-Catégorie'), 
            'title': _('Titre'),
            'description': _('Description'),
            'is_published': _('Est Publié'),
        }



class IsPublished(forms.ModelForm):
    is_published = forms.BooleanField(label="est publié", required=False)
    class Meta:
        model = Article
        fields = [
            'is_published',
        ]





# class MediaUpdateForm(forms.ModelForm):
#     # file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
#     class Meta:

#         model = Medias
#         exclude = ('article', 'category', 'sub_category', 'description')
#         fields = [
#             'category', 
#             'sub_category', 
#             'title', 
#             'description',
#             'media', 
#         ]
#         labels = {
#             'category': 'Catégorie',
#             'sub_category': 'Sous Catégorie', 
#             'title':'Titre',
#             'description': 'Description',
#             'media':'Média',
#         }


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre Commentaire', 'rows':'1', 'cols':'50' }))
    class Meta: 
        model = Comment 
        fields = [
            'content',
        ]
        labels = {
            'content': _('Commentaire')
        }


class ReplyCommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre Commentaire', 'rows':'1', 'cols':'40' }))
    class Meta: 
        model = Comment 
        fields = [
            'reply',
        ]
        labels = {
            'reply': _('Répondre')
        }