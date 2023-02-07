from django.urls import path 
from .views import RegisterUserView,UserLogin,EmailVerificationAPI,EmailVerificationOTPAPI

urlpatterns = [
    path('register-user',RegisterUserView.as_view(), name="register-user'"),
    path('login',UserLogin.as_view(), name='login'),
    path('email-verification/', EmailVerificationAPI.as_view(), name='email-verification'),
    path('email-verification-otp/', EmailVerificationOTPAPI.as_view(), name='email-verification-otp'),

] 