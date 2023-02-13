from rest_framework import generics
from .serializers import PatientProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .permissions import IsPatient
from .models import PatientProfile

# Create your views here.

class CreatePatientProfileView(generics.ListCreateAPIView):
    serializer_class = PatientProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsPatient]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RetrieveUpdatePateintProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsPatient]

    def get_object(self):
        user = self.request.user
        return PatientProfile.objects.get(user=user)