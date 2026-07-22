from users.models import User
from users.serializers.address_serializer import AddressSerializer
from users.serializers.telephone_serializer import TelephoneSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    telephones = TelephoneSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'user_type',
            'average_rating',
            'total_ratings',
            'cancellations_month',
            'addresses',
            'telephones'
        ]

class UserServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'user_type'
        ]