from services.models import Service
from services.serializers.service_serializer import ServiceSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Service"],
    summary="Listagem de todos os serviços",
    description="Retorna uma listagem de todos os serviços cadastrados no sistema",
)
class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(
    tags=["Service"],
    summary="Detalhes de um serviço",
    description="Retorna os detalhes de um serviço cadastrado no sistema",
)
class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
