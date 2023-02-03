from django.urls import path
from .views import DoctorProfileView,SlotListCreateAPIView, SlotRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('profile/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('slots/', SlotListCreateAPIView.as_view(), name='slot_list_create'),
    path('slots/<int:pk>/', SlotRetrieveUpdateDestroyAPIView.as_view(), name='slot_retrieve_update_destroy')
]