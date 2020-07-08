from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.db.models import Avg, Count

from django.db.models import F, Q, When
from .filters import ArticleFilter

from django.core.files.images import get_image_dimensions

from django.urls import reverse_lazy, reverse

import os
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
# from .forms import LoginForm, UserRegistrationForm
from django.utils.translation import gettext as _
from .forms import *
from .tokens import account_activation_token
from .models import *
from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory

from django.utils.timezone import datetime
from django.core.paginator import Paginator


# messages.debug 
# messages.info 
# messages.success
# messages.warning 
# messages.error

# django-admin makemessages -l en
# django-admin compilemessages 


# ====================== Register ==================================== 

def sign_up(request):
    context = {}

    users = User.objects.all()

    # Email Unique for User
    emails = []
    for user in users:
        emails += user.email,
    # print('emails =====: ', emails)
    
    if request.method == 'POST':
       
        form = SignUpForm(request.POST or None)

        user_email = request.POST.get('email')
        # print("User Email ====== : " + user_email)

        if user_email not in emails:
            print("===== True")
            
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # form.save()

                current_site = get_current_site(request)
                subject = 'Activate Your Account.'
                message = render_to_string('register/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    subject, message, to=[to_email]
                )
                email.send()

                username = form.cleaned_data.get('username')            
                # raw_password = form.cleaned_data.get('password1')
                # user = authenticate(username=username, password=raw_password)

                messages.success(request, f'Your Account has been created Successful with username {username} !, Please confirm your email address to complete the registration ')
                
                # login(request, user)
                return redirect('login')



                # user = form.save(commit=False)
                # user.is_active = False
                # user.save()
               

                # user.email_user(subject, message)

                # # user.refresh_form_db()
                # user.profile.birth_date = form.cleaned_data.get('birth_date')
                # user.save()

                # username = form.cleaned_data.get('username')
                # raw_password = form.cleaned_data.get('password1')
                # user = authenticate(username=user.username, password=raw_password)
                # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                # return redirect('account_activation_sent')
        else:
            print(" ======= False")

            if user_email in emails:
                messages.warning(request, f'Please Sign-up with another email address, this email {user_email} is already in use')
                return redirect('register')
            # else:
                

                
    else:
        form = SignUpForm()
        
    context['form']=form
    return render(request, 'register/register.html', context)



def account_activation_sent(request):
    return render(request, 'register/activation.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'register/active.html')





@login_required(login_url='login')
def profile(request, user_id):
    articles_is_pub = Article.objects.filter(auther=user_id).filter(is_published=True)
    articles_not_pub = Article.objects.filter(auther=user_id).filter(is_published=False)

    user = request.user
    favourite_article = user.favorites.all()
        
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated successfully ')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'articles_is_pub' : articles_is_pub,
        'articles_not_pub' : articles_not_pub,
        'favourite_article': favourite_article,
    }
    
    
    return render(request, 'register/profile.html', context)
    

# def user_login (request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
            
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('home')
#                     # return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'register/login.html', {'form': form})



# @login_required
# def dashboard(request):
#     return render(request,
#                   'account/dashboard.html',
#                   {'section': 'dashboard'})



# def LogoutView(request):
#     pass



# ==================== Article & CRUD ======================== 
def home(request):

    # User language
    # from django.utils import translation
    # user_language = 'fr'
    # translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    # if translation.LANGUAGE_SESSION_KEY in request.session:
    #     del request.session[translation.LANGUAGE_SESSION_KEY]

    

    articles_list = Article.objects.all().order_by("-date_published")
    users_num = User.objects.all().count()

    num_articles_pub = Article.objects.filter(is_published=True).count()
    num_articles_n_pub = Article.objects.filter(is_published=False).count()

    # num_articles = len(articles_list)

    # Search 
    # query = request.GET.get('q')
    # if query:
    #     articles_list = Article.objects.filter(
    #         Q(title__icontains=query)|
    #         Q(category=query)|
    #         Q(auther_username=query)|
    #         Q(description__icontains=query)
    #     )


#    user_like = Article.likes.all()
#    print(user_like)

    # Search 
    # query = request.GET.get('q')
    # if query:
    myFilter = ArticleFilter(request.GET, queryset=articles_list)
    articles_list = myFilter.qs



    # ======== Pagination ===============  
    # paginator = Paginator(articles_list, 100)
   
    # try:
    #     page = int(request.GET.get('page', '1'))
    # except:
    #     page = 1

    # try: 
    #     articles = paginator.page(page)
    # except(EmptyPage, InvalidPage):
    #     articles = paginator.page(paginator.num_pages)



    # =============== Request ==============
    if request.method == 'POST':
        form_new_article = ArticleForm(request.POST or None, request.FILES or None)
        form_new_media = MediaForm(request.POST or None, request.FILES or None)

        if form_new_article.is_valid() and form_new_media.is_valid():

            article = form_new_article.save(commit=False)
            article.auther = request.user
            article.save()
            form_new_article = ArticleForm()
        

            for field in request.FILES.keys():
                filename = request.FILES[field]
                for formfile in request.FILES.getlist(field):
                    img = Medias(article=article, media=formfile)
                    img.auther = request.user
                    img.title = article.title
                    img.save()
                    form_new_media = MediaForm()

            messages.success(request, 'Your have bin successefully clreate Article')
            

    else:
        form_new_article = ArticleForm()
        form_new_media = MediaForm()

    context = {
            'form_new_article': form_new_article,
            'form_new_media': form_new_media,

            # 'articles': articles,
            'articles_list': articles_list,
            # 'num_articles': num_articles,
            'num_articles_pub': num_articles_pub,
            'num_articles_n_pub': num_articles_n_pub,
            'myFilter': myFilter, 
            'users_num': users_num,
        }

    return render(request, 'article/home.html', context)

# https://medium.com/@angiegemes/upload-multiple-images-to-db-from-a-django-form-f230954c77e3




@login_required(login_url='login')
def like(request, pk):
    article = get_object_or_404(Article, id=request.POST.get('article_id'))
    
    # liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True

    context = {
        'article': article,
        # 'medias': medias,
        # 'total_likes': total_likes,
        # 'liked': liked,
    }

    # if request.is_ajax():
    #     html = render_to_string('article/detail.html', context, request=request)
    #     return JsonResponse({'form': html})

    # return HttpResponseRedirect(reverse('home'), args=[str(pk)])
    return redirect('home')


@login_required(login_url='login')
def favorite(request, pk):
    article = get_object_or_404(Article, id=request.POST.get('article_id'))

    if article.favorites.filter(id=request.user.id).exists():
        article.favorites.remove(request.user)
        favoreted = False
    else:
        article.favorites.add(request.user)
        favoreted = True
    
    context = {
        'article': article,
    }
    return redirect('home')
    # return HttpResponseRedirect(article.get_absolute_url())



@login_required(login_url='login')
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))

    if comment.comment_likes.filter(id=request.user.id).exists():
        comment.comment_likes.remove(request.user)
        comment_liked = False
    else:
        comment.comment_likes.add(request.user)
        comment_liked = True

    context = {
        'comment': comment,
    }

    return redirect('home')



@login_required(login_url='login')
def like_reply(request, pk):
    reply = get_object_or_404(Comment, id=request.POST.get('reply_id'))

    if reply.reply_likes.filter(id=request.user.id).exists():
        reply.reply_likes.remove(request.user)
        reply_liked = False
    else:
        reply.reply_likes.add(request.user)
        reply_liked = True

    context = {
        'reply': reply,
    }

    return redirect('home')
    


def detail_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article= article, reply=None).order_by('-id')

    # print('==========', article.auther.profile.created_at)

    # medias = Media.objects.filter(article_id=article)
    total_likes = article.total_likes()
    total_favorites = article.total_favorites()
    

    liked = False
    if article.likes.filter(id=request.user.id).exists():
        liked = True
    
    favoreted = False
    if article.favorites.filter(id=request.user.id).exists():
        favoreted = True


    
    # comment_liked = False
    # if comment.comment_likes.filter(id=request.user.id).exists():
    #     comment_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            # reply 
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(article=article, auther=request.user, content=content, reply=comment_qs)
            comment.save()
            
    else:
        comment_form = CommentForm()

    context = {
        'article': article,
        # 'medias': medias,
        'total_likes': total_likes,
        'liked': liked,
        'comments': comments, 
        'comment_form': comment_form,

        'favoreted': favoreted,
        'total_favorites': total_favorites,
        # 'user_like': user_like,
        
    }
    

    return render(request, 'article/detail.html', context)



# =============== Update ====================== 
@login_required(login_url='login')
def update_article(request, article_id):

    article = get_object_or_404(Article, id=article_id)
    ImageFormset = modelformset_factory(Medias, fields=('media', ), extra=0)

    if article == None:
        return HttpResponse('Article not found')
    else:        
        if request.method == 'POST':

            form_update_article = ArticleForm(request.POST or None,  instance=article) 
            form_update_media = ImageFormset(request.POST or None, request.FILES or None)
            form_new_media = MediaForm(request.POST or None, request.FILES or None)
            
            form_is_published = IsPublished(request.POST or None, instance=article)
            

           
            if form_update_article.is_valid() and form_update_media.is_valid() and form_new_media.is_valid() and form_is_published.is_valid():
                article = form_update_article.save(commit=False)
                article.date_updated = datetime.utcnow()
                article.save()

                # print('form data =======', form_update_media.cleaned_data)
                
                data= Medias.objects.filter(article=article)

                # =================== Update and Delete Media =====================
                for index, f in enumerate(form_update_media):
                    if f.cleaned_data:
                        # ========= for add new media with the arg (extra=1) ==========
                        if f.cleaned_data['id'] is None:
                            photo = Medias(article=article, media=f.cleaned_data.get('media')) 
                            photo.title = article.title
                            photo.auther = request.user
                            photo.save()
                        # for Delete an media
                        elif f.cleaned_data['media'] is False:
                            photo = Medias.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                            photo.delete()
                        # for Update an media
                        else:
                            photo = Medias(article=article, media=f.cleaned_data.get('media'))
                            d = Medias.objects.get(id=data[index].id)
                            d.auther = request.user
                            d.media = photo.media
                            d.date_updated = datetime.utcnow()
                            d.save()


                # ============== New Media ==================','
                for field in request.FILES.keys():
                    for formfile in request.FILES.getlist(field):
                        img = Medias(article=article, media=formfile)
                        img.auther = request.user
                        img.title = article.title
                        img.save()

                return redirect('home')

                if request.user.is_superuser:
                    form_is_published.save()

        else:
            form_update_article = ArticleForm(instance=article)
            form_update_media = ImageFormset(queryset=Medias.objects.filter(article_id=article))
            form_new_media = MediaForm()
            form_is_published = IsPublished(instance=article)

            

        context = {
            'form_update_article': form_update_article, 
            'form_update_media': form_update_media,
            'form_new_media': form_new_media,
            'article': article, 
            'form_is_published': form_is_published,
        }

        return render(request, 'article/update_article.html', context)







@login_required(login_url='login')
def delete_article(request, article_id):
    article = get_object_or_404(Article ,id=article_id)
    if request.method == 'POST':
        if article == None:
            return HttpResponse('Article not found')
        else:
            article.delete()
            return redirect('home')

    context = {
        'article': article
    }

    return render(request, 'article/delete_article.html', context)









# ==================== Category & CRUD ========================
@login_required(login_url='login')
def category(request):
    form_new_category = CategoryForm(request.POST or None)
    if form_new_category.is_valid():
        form_new_category.save()
        form_new_category = CategoryForm()

    categories = Category.objects.all()

    context = {
        'form_new_category': form_new_category,
        'categories': categories,
    }

    return render(request, 'article/category.html', context)


@login_required(login_url='login')
def update_category(request, category_id):
    category=Category.objects.get(id=category_id)
    if category == None:
        return HttpResponse("Category not found")
    else:
        form_update_category = CategoryForm(request.POST or None, instance=category)  
        if form_update_category.is_valid():  
            form_update_category.save() 
            return redirect('category')

    context = {
        'form_update_category': form_update_category,
        'category': category,
    }

    return render(request, 'article/update_category.html' , context)


@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        if category == None:
            return HttpResponse("Category not found")
        else:
            category.delete()
            return redirect('category')
    context = {
        'category': category,
    }
    return render(request, 'article/delete_category.html', context)






# ==================== Sub_Category & CRUD ========================
@login_required(login_url='login')
def sub_category(request):
    form_new_subcategory = SubCategoryForm(request.POST or None)
    if form_new_subcategory.is_valid():
        form_new_subcategory.save()
        form_new_subcategory = CategoryForm()

    sub_categories = SubCategory.objects.all()

    context = {
        'form_new_subcategory': form_new_subcategory,
        'sub_categories': sub_categories,
    }

    return render(request, 'article/sub_category.html', context)



@login_required(login_url='login')
def update_sub_category(request, sub_category_id):
    sub_category=SubCategory.objects.get(id=sub_category_id)
    if sub_category == None:
        return HttpResponse("Sub Category not found")
    else:
        form_update_sub_category = SubCategoryForm(request.POST or None, instance = sub_category)  
        if form_update_sub_category.is_valid():  
            form_update_sub_category.save() 
            return redirect('sub_category')
    
    context = {
        'form_update_sub_category': form_update_sub_category,
        'sub_category': sub_category
    }
    return render(request, 'article/update_sub_category.html', context)



@login_required(login_url='login')
def delete_sub_category(request, sub_category_id):
    sub_category = get_object_or_404(SubCategory, id=sub_category_id)
    if request.method == 'POST':
        if sub_category == None:
            return HttpResponse("Sub Category not found")
        else:
            sub_category.delete()
            return redirect('sub_category')
    context = {
        'sub_category': sub_category,
    }
    return render(request, 'article/delete_sub_category.html', context)


# =========== Page 404 ==================
def page_not_found_view(request, exception):
     return render(request,'errors/404.html')









# =============== DashBoard =================
@login_required(login_url='login')
def home_dashboard(request):
    articles = Article.objects.all().order_by("-date_published")
    users_num = User.objects.all().count()
    
    # ========= Start Date Sitting ============ 
    # date_start = datetime.utcnow
    now = datetime.now()

    day = now.strftime("%d")
    month = now.strftime("%m")
    year = now.strftime("%Y")
    time = now.strftime("%H:%M:%S")

    start_date = year+'-'+month+'-'+'01'+' '+'00:00:00'
    end_date = year+'-'+month+'-'+day+' '+time

    # start_date_juin = year+'-'+'06'+'-'+'01'+' '+'00:00:00'
    # end_date_juin = year+'-'+'06'+'-'+'30'+' '+'23:59:59'

    start_date_year = year+'-'+'01'+'-'+'01'+' '+'00:00:00'
    end_date_year = year+'-'+'12'+'-'+'31'+' '+'23:59:59'
    # ========= End Date Sitting ============
    

    # statestique -> auther : num_articles
    # Actuel
    articles_filter = Article.objects.filter(Q(date_published__gte=start_date)&Q(date_published__lte=end_date))
    authors = User.objects.filter(article_auther__in=articles_filter).annotate(num_articles=Count('id'))

    # toute la née
    articles_filter_year = Article.objects.filter(Q(date_published__gte=start_date_year)&Q(date_published__lte=end_date_year))
    authors_year = User.objects.filter(article_auther__in=articles_filter_year).annotate(num_articles=Count('id'))


    # Juin
    # articles_filter_juin = Article.objects.filter(Q(date_published__gte=start_date_juin)&Q(date_published__lte=end_date_juin))
    # authors_juin = User.objects.filter(article_auther__in=articles_filter_juin).annotate(num_articles=Count('id'))

    # statestique -> auther : num_comments
    # Actuel
    comments = Comment.objects.filter(Q(comment_at__gte=start_date)&Q(comment_at__lte=end_date))
    author_comments = User.objects.filter(user_comment__in=comments).annotate(num_comments=Count('id'))

    # toute la née
    comments_year = Comment.objects.filter(Q(comment_at__gte=start_date_year)&Q(comment_at__lte=end_date_year))
    author_comments_year = User.objects.filter(user_comment__in=comments_year).annotate(num_comments=Count('id'))

    # Juin
    # comments_juin = Comment.objects.filter(Q(comment_at__gte=start_date_juin)&Q(comment_at__lte=end_date_juin))
    # author_comments_juin = User.objects.filter(user_comment__in=comments_juin).annotate(num_comments=Count('id'))

    # ========= Nome de la mois ==========  
    if month == '01':
        month = 'Janvier'
    elif month == '02':
        month = 'Février'
    elif month == '03':
        month = 'Mars'
    elif month == '04':
        month = 'Avril'
    elif month == '05':
        month = 'Mai'
    elif month == '06':
        month = 'Juin'
    elif month == '07':
        month = 'Juillet'
    elif month == '08':
        month = 'Août'
    elif month == '09':
        month = 'Septembre'
    elif month == '10':
        month = 'Octobre'
    elif month == '11':
        month = 'Novembre'
    elif month == '12':
        month = 'Décembre'
        


    context = {
        'articles': articles, 
        'authors': authors,
        'author_comments': author_comments,

        'authors_year': authors_year,
        'author_comments_year': author_comments_year,

        'month' : month,
        'year': year,
        'users_num' : users_num,

    }
    return render(request, 'dashboard/dashboard.html', context)








# dashboard article detail 
@login_required(login_url='login')
def dash_detail_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    

    context = {
        'article': article,
    }
    

    return render(request, 'dashboard/detai.html', context)




@login_required(login_url='login')
def functions_dashboard(request):
    users = User.objects.all()
    # profile = Profile.objects.all()


    context = {
        'users': users,
        # 'profile': profile,
    }
    return render(request, 'dashboard/functions.html', context)




@login_required(login_url='login')
def userConfigurations(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # profile = Profile.objects.all()

    if request.method == 'POST' and request.user.is_superuser:
        user_conf_form = UserUpdateConfForm(request.POST or None, instance=user)
        user_conf_comment_form = UserCommentForm(request.POST or None, instance=user.profile)

        if user_conf_form.is_valid() and user_conf_comment_form.is_valid():
            user_conf_form.save()
            user_conf_comment_form.save()

            return redirect('functions')
    else:
        user_conf_form = UserUpdateConfForm(instance=user)
        user_conf_comment_form = UserCommentForm(instance=user.profile)

    context = {
        'user': user,
        'user_conf_form': user_conf_form,
        'user_conf_comment_form': user_conf_comment_form,
    }
    return render(request, 'dashboard/userConfiguration.html', context)


@login_required(login_url='login')
def delUser(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST' and request.user.is_superuser:
        user.delete()

        messages.success(request, f"L’utilisateur ' { user } ' est supprimé")

        return redirect('functions')

    context = {
        'user': user,
    }


    return render(request, 'dashboard/delete_user.html', context)




# dashboard update article
# @login_required(login_url='login')
# def dash_update_article(request, article_id):

#     article = get_object_or_404(Article, id=article_id)
#     ImageFormset = modelformset_factory(Medias, fields=('media', ), extra=0)

#     if article == None:
#         return HttpResponse('Article not found')
#     else:
        
#         if request.method == 'POST':

#             form_update_article = UpdateArticleForm(request.POST or None,  instance=article) 
#             form_update_media = ImageFormset(request.POST or None, request.FILES or None)
#             form_new_media = MediaForm(request.POST or None, request.FILES or None)

           
#             if form_update_article.is_valid() and form_update_media.is_valid() and form_new_media.is_valid():
#                 article = form_update_article.save(commit=False)
#                 article.date_updated = datetime.utcnow()
#                 article.save()

#                 # print('form data =======', form_update_media.cleaned_data)
                
#                 data= Medias.objects.filter(article=article)

#                 # =================== Update and Delete Media =====================
#                 for index, f in enumerate(form_update_media):
#                     if f.cleaned_data:
#                         # ========= for add new media with the arg (extra=1) ==========
#                         if f.cleaned_data['id'] is None:
#                             photo = Medias(article=article, media=f.cleaned_data.get('media')) 
#                             photo.title = article.title
#                             photo.auther = request.user
#                             photo.save()
#                         # for Delete an media
#                         elif f.cleaned_data['media'] is False:
#                             photo = Medias.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
#                             photo.delete()
#                         # for Update an media
#                         else:
#                             photo = Medias(article=article, media=f.cleaned_data.get('media'))
#                             d = Medias.objects.get(id=data[index].id)
#                             d.auther = request.user
#                             d.media = photo.media
#                             d.date_updated = datetime.utcnow()
#                             d.save()


#                 # ============== New Media ==================','
#                 for field in request.FILES.keys():
#                     for formfile in request.FILES.getlist(field):
#                         img = Medias(article=article, media=formfile)
#                         img.auther = request.user
#                         img.title = article.title
#                         img.save()

#                 return redirect('dashboard')
#         else:
#             form_update_article = UpdateArticleForm(instance=article)
#             form_update_media = ImageFormset(queryset=Medias.objects.filter(article_id=article))
#             form_new_media = MediaForm()

            

#         context = {
#             'form_update_article': form_update_article, 
#             'form_update_media': form_update_media,
#             'form_new_media': form_new_media,
#             'article': article
#         }

#         return render(request, 'dashboard/update_article.html', context)









# (\__/)
# (='.'=)This is Bunny. Copy and paste bunny
# (")_(") to help him gain world domination.
