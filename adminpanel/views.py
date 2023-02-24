from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


from account.models import Account
from .serializers import AdminDoctorApprovalSerializer, DoctorListSerializer, DoctorDetailSerializer
from doctors.serializers import DoctorProfileSerializer
from doctors.models import DoctorProfile



class USerApprovalAPIView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AdminDoctorApprovalSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Account, pk=pk)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        if request.data.get('is_approved') == 'True':
            user.is_approved = True
            user.save()
            return Response({'message': 'User has been Approved.'}, status=status.HTTP_200_OK)

        else:
            user.is_approved = False
            user.save()
            return Response({'message': 'User has been Disapproved.'}, status=status.HTTP_200_OK)
            
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 1


class DoctorListAPIView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'department__name']
    ordering_fields = ['user__full_name', 'department__name', 'user__is_approved']

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department', None)
        approved = self.request.query_params.get('approved', None)

        if department:
            queryset = queryset.filter(department__name=department)

        if approved is not None:
            queryset = queryset.filter(user__is_approved=approved)

        queryset = queryset.order_by('user__first_name')

        return queryset

class DoctorDetailAPIView(generics.RetrieveAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorDetailSerializer
    permission_classes = [IsAdminUser]