from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
from . import views
from django.urls import re_path
# handler404 = 'accounts.views.custom_404'

urlpatterns = [
    path('', views.home, name='home'),

    path('login', views.login_view, name='login'),
    path('registration', views.registration_view, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-password/', views.update_password, name='update_password'),
    path('update-profile-pic/', views.update_profile_pic, name='update_profile_pic'),

    
    path('forget_Message', views.ForgetMessage, name='forget_Message'),
    path('forget-password/' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),

]
