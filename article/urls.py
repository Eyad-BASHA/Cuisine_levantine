from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views
from django.views.generic import TemplateView
# from .views import BasicFileUploadView


urlpatterns = [
    # ========= User Auth 
    path('register/', views.sign_up, name='register'),

    path('account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    path('login/', auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='register/logged_out.html'), name='logout'),
    path('profile/<str:user_id>', views.profile, name='profile'),

    # Password Reset 
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='register/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='register/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/done/', auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_complete.html'), name='password_reset_complete'),

    # Password Reset 
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='register/password_change_done.html'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='register/password_change.html'), name='password_change'),

    # ========= Articles 
    path('', views.home, name='home'),
    path('detail_article/<str:article_id>', views.detail_view, name='detail_article'),
    path('update_article/<str:article_id>', views.update_article, name='update_article'),
    path('delete_article/<str:article_id>', views.delete_article, name='delete_article'),
    path('category', views.category, name='category'),
    path('update_category/<str:category_id>', views.update_category, name='update_category'),
    path('delete_category/<str:category_id>', views.delete_category, name='delete_category'),
    path('sub_category', views.sub_category, name='sub_category'),
    path('update_sub_category/<str:sub_category_id>', views.update_sub_category, name='update_sub_category'),
    path('delete_sub_category/<str:sub_category_id>', views.delete_sub_category, name='delete_sub_category'),
    path('like_article/<int:pk>', views.like ,name='like_article'),
    path('like_comment/<int:pk>', views.like_comment ,name='like_comment'),
    path('like_reply/<int:pk>', views.like_reply ,name='like_reply'),
    path('favor_article/<int:pk>', views.favorite ,name='favor_article'),

    # ========= DashBoard =========
    path('dashboard', views.home_dashboard, name='dashboard'),
    path('dash_detail_article/<str:article_id>', views.dash_detail_view, name='dash_detail_article'),
    # path('dash_update_article/<str:article_id>', views.dash_update_article, name='dash_update_article'),
    path('functions', views.functions_dashboard, name='functions'),
    path('user_conf/<str:user_id>', views.userConfigurations, name='user_conf'),
    path('delete_user/<str:user_id>', views.delUser, name='delete_user'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

