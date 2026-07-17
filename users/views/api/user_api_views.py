from users.models import User
from users.serializers.user_serializer import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=['User'], 
    summary='Listagem de usuários', 
    description='Endpoint para listagem de todos os usuários',
)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(
    tags=['User'],
    summary='Detalhes de um usuário',
    description='Endpoint para detalhes de um usuário especifico',
)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]