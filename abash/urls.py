from django.urls import path, include
from abash.views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns =[
    #path('login_details/<int:pk>',login_settings),
    path('user_details/<int:pk>',user_settings),
    path('login_create/', login_create),
    path('login/', obtain_auth_token),
    path('logout/', logout_view),
    path('add_property/property', add_property),
    path('get_property/<int:arg>', get_property),
    path('add_property/more_images', add_property_image),
    path('get_property_images/<int:arg>', get_property_images),
    path('add_property/room', add_room),
    path('get_room/<int:arg>', get_room),
    path('add_property/location', add_location),
    path('get_location/<int:arg>', get_location),
    path('app_rating/',app_rating),
    path('get_app_rating/',get_app_rating),
    path('property_rating/',property_rating),
    path('get_property_rating/',get_property_rating),
    path('property_filtering',filter_property),
    path('property_search/<slug:search_topic>',location_search),
    path('request_booking/', request_booking),
    path('user_booking/<int:user_id>',user_get_booking),
    path('owner_booking/<int:owner_id>',owner_get_booking),
    path('confirm_booking/<int:arg>',confirm_booking),
    path('reject_received_booking/<int:arg>',reject_received_booking),
    path('reject_requested_booking/<int:arg>',reject_requested_booking),
    path('current_home/<int:user_id>',user_current_home),
    path('added_propertys/<int:user_id>',owners_added_propertys),
    path('add_wishlist/',add_delete_wishlist),
    path('remove_wishlist/',add_delete_wishlist),
    path('get_wishlist/<int:user_id>',get_wishlist)

]