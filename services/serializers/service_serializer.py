from services.models import Service
from services.serializers.category_serializer import ServiceCategorySerializer
from users.serializers.user_serializer import UserServiceSerializer
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer()
    client = UserServiceSerializer()
    provider = UserServiceSerializer()
    displacement_start = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    displacement_end = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Service
        fields = [
            'id',
            'category',
            'description',
            'status',
            'price',
            'payment_method',
            'displacement_start',
            'displacement_end',
            'created_at',
            'updated_at',
            'client',
            'provider',
        ]
