from django.urls import path
from property import views


urlpatterns = [
    path("Property_list",views.Property_list,name="Property_list"),
    path("myProperty",views.myProperty,name="myProperty"),

    path('hosting/<str:info_type>/', views.Hosting, name='Hosting'),


    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path("property/edit/<int:property_id>/", views.edit_property, name="edit_property"),



    # path('myReservation/', views.Hosting, name='Hosting'),
    # path('Hosting/my_listings/', views.Hosting, {'info_type': 'my_listings'}, name='my_listings'),
    # path('Hosting/pending_requests/', views.Hosting, {'info_type': 'pending_requests'}, name='pending_requests'),
    # path('Hosting/upcoming_reservations/', views.Hosting, {'info_type': 'upcoming_reservations'}, name='upcoming_reservations'),
    # path('Hosting/currently_hosting/', views.Hosting, {'info_type': 'currently_hosting'}, name  ='currently_hosting'),
    # path('Hosting/checked_out/', views.Hosting, {'info_type': 'checked_out'}, name='checked_out'),

    path("stays/",views.stays,name="stays"),
    path("stays/<str:property_type>/",views.stays_type,name="stays_type"),
    path('stays/city/<str:city_name>/', views.staysByCity, name='stays_by_city'),
    path('search/', views.search, name='search'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('submit_review/<int:property_id>/', views.submit_review, name='submit_review'),
    path('book/<int:booking_id>/', views.book, name='book'),
    path('about', views.about, name='about'),

    path('accept-reservation/<int:booking_id>/', views.accept_reservation, name='accept_reservation'),
    path('decline-reservation/<int:booking_id>/', views.decline_reservation, name='decline_reservation'),
    # path('confirm-reservation/<int:booking_id>/', views.confirm_reservation, name='confirm_reservation'),

    path('filter_property', views.filter_property, name='filter_property'),

    path('my-booking', views.my_booking, name='my_booking'),

    path('search_properties/', views.search_properties, name='search_properties'),
    path('search_map/', views.search_map, name='search_map'),

]
