from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from account.models import Account
from .models import DoctorProfile, Slot
from .serializers import DoctorProfileSerializer, SlotSerializer
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor, IsApproved



class DoctorProfileView(APIView):
    """API for the doctors to update and edit their profile"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor_profile = DoctorProfile.objects.get(user=request.user)
        serializer = DoctorProfileSerializer(doctor_profile)
        return Response(serializer.data)


    def patch(self, request):
        doctor_profile = DoctorProfile.objects.get(user_id=request.user.id)
        serializer = DoctorProfileSerializer(doctor_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlotListCreateAPIView(generics.ListCreateAPIView):
    """API for doctors to get the slots and create new ones"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor, IsApproved]

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def perform_create(self, serializer):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        serializer.save(doctor=doctor)

class SlotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API for the doctors to get, edit and delete the slots"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor, IsApproved]

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer