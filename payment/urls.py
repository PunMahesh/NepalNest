from django.urls import path
from payment import views

urlpatterns = [
    path('initiate-khalti', views.initiate_khalti, name='initiate-khalti'),
    path('return_url/<int:booking_id>/', views.return_url, name="return_url"),
]
