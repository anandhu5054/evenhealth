from django.urls import path 
from . import views

urlpatterns = [
    path('register-user', views.RegisterUserView.as_view(), name="register-user'"),
    path('login',views.UserLogin.as_view(), name='login')

] 