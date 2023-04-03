from django.urls import path
from .views import (
    # DoctorProfileView,
    SlotListCreateAPIView, 
    SlotRetrieveUpdateDestroyAPIView,
    CreateDoctorProfileview,
    CreateDepartmentView,
    CreateQualificationView,
    RetrieveUpdateDoctorProfileView,
    RetrieveDepartmentView,
    BookedAppointmentsAPIView

)

urlpatterns = [
    path('register/', CreateDoctorProfileview.as_view(), name='doctor-profile'),
    path('create-dept/', CreateDepartmentView.as_view(), name='doctor-profile'),
    path('departments/<int:pk>/', RetrieveDepartmentView.as_view(), name='retrieve_department'),
    path('add-qualification/', CreateQualificationView.as_view(), name='doctor-profile'),
    path('get_or_update-profile/', RetrieveUpdateDoctorProfileView.as_view(), name='get_or_update-profile'),
    path('slots/', SlotListCreateAPIView.as_view(), name='slot_list_create'),
    path('slots/<int:pk>/', SlotRetrieveUpdateDestroyAPIView.as_view(), name='slot_retrieve_update_destroy'),
    path('bookings', BookedAppointmentsAPIView.as_view(), name='bookings')
]