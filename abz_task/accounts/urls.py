from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

from .views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
