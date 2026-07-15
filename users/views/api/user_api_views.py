from users.models import User
from users.serializers.user_serializer import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]