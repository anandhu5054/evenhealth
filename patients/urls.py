from django.urls import path
from .views import (
    CreatePatientProfileView, 
    RetrieveUpdatePateintProfileView, 
    DoctorListForPatientsAPIView, 
    DoctorDetailAPIView, 
    SlotsOfDoctorsAPIView
)


urlpatterns = [
    path('register/', CreatePatientProfileView.as_view(), name='patient-profile'),
    path('get_or_update-profile/', RetrieveUpdatePateintProfileView.as_view(), name='get_or_update-profile'),
     path('doctors/', DoctorListForPatientsAPIView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),
    path('slots/', SlotsOfDoctorsAPIView.as_view(), name='slot-list'),
]