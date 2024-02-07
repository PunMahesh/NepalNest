from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("login",views.login_view,name="login"),
    path("registration",views.register_view,name="registration"),
]
