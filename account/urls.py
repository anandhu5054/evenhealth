from django.urls import path 
from . import views

urlpatterns = [
    path('register-patient', views.RegisterPatientView.as_view(), name="register-patient'"),
    path('register-doctor', views.RegisterDoctortView.as_view(), name="register-doctor'"),
    path('register-lab', views.RegisterLabView.as_view(), name="register-lab'"),
    path('login',views.UserLogin.as_view(), name='login')

] 