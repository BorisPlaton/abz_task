from django.urls import path, include
from . import views

import django.contrib.auth.urls

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.RegisterView.as_view(), name='register')
]
