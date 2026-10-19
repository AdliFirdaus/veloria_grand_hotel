from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('<uuid:pk>/', views.room_detail, name='room_detail'),
    path('create/', views.room_create, name='room_create'),
    path('<uuid:pk>/edit/', views.room_update, name='room_update'),
    path('<uuid:pk>/delete/', views.room_delete, name='room_delete'),
]
