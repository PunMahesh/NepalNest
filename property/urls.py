from django.urls import path
from property import views


urlpatterns = [
    path("Property_list",views.Property_list,name="Property_list"),
    path("myProperty",views.myProperty,name="myProperty"),

]
