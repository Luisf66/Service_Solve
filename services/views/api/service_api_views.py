from services.models import Service
from services.serializers.service_serializer import ServiceSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
