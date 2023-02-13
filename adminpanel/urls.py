from django.urls import path
from .views import USerApprovalAPIView, DoctorListAPIView, DoctorDetailAPIView

urlpatterns =[
    path('user/<int:pk>/approve-or-disapprove/',USerApprovalAPIView.as_view(), name='user-approve-disapprove'),
    path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),
]