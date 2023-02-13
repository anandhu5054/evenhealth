from django.urls import path
from .views import CreatePatientProfileView, RetrieveUpdatePateintProfileView


urlpatterns = [
    path('register/', CreatePatientProfileView.as_view(), name='doctor-profile'),
    path('get_or_update-profile/', RetrieveUpdatePateintProfileView.as_view(), name='get_or_update-profile'),
]