# pred/urls.py
# pred/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_index, name='login')  # Use an empty string for the base URL of 'pred/'
]
