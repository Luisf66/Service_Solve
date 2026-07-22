from services.models import ServiceCategory
from rest_framework import serializers


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = [
            'name',
            'description'
        ]