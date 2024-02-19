from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
from . import views
from django.urls import re_path
# handler404 = 'accounts.views.custom_404'

urlpatterns = [
    # path("login",views.login_view,name="login"),
    # path("registration",views.registration_view,name="registration"),
    path('logout/', views.logout_view, name='logout'),
    # URL pattern for the login view
    path('', views.home, name='home'),

    path('login', views.login_view, name='login'),

    # URL pattern for the registration view
    path('registration', views.registration_view, name='registration'),



]
