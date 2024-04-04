from django.urls import path
from property import views


urlpatterns = [
    path("Property_list",views.Property_list,name="Property_list"),
    path("myProperty",views.myProperty,name="myProperty"),
    path("stays/",views.stays,name="stays"),
    path("stays/<str:property_type>/",views.stays_type,name="stays_type"),
    path('search/', views.search, name='search'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('submit_review/<int:property_id>/', views.submit_review, name='submit_review'),
    path('book/<int:booking_id>/', views.book, name='book'),
    path('payment', views.payment, name='payment'),
    path('about', views.about, name='about'),
    path('accept-reservation/<int:booking_id>/', views.accept_reservation, name='accept_reservation'),
    path('decline-reservation/<int:booking_id>/', views.decline_reservation, name='decline_reservation'),
    # path('confirm-reservation/<int:booking_id>/', views.confirm_reservation, name='confirm_reservation'),

    path('filter_property', views.filter_property, name='filter_property'),

]
