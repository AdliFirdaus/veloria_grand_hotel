from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('test-error-400/', views.test_error_400, name='test_error_400'),  # For testing 400 error
    path('test-error-403/', views.test_error_403, name='test_error_403'),  # For testing 403 error
    path('test-error-404/', views.test_error_404, name='test_error_404'),  # For testing 404 error
    path('test-error-500/', views.test_error_500, name='test_error_500'),  # For testing 500 error
]
