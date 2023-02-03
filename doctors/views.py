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
from .permissions import IsDoctor



class DoctorProfileView(APIView):

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
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

class SlotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer