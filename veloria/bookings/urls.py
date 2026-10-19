from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('create/<uuid:room_pk>/', views.booking_create, name='booking_create'),
    path('<uuid:pk>/', views.booking_detail, name='booking_detail'),
    path('<uuid:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('<uuid:pk>/status/', views.booking_update_status, name='booking_update_status'),
]
