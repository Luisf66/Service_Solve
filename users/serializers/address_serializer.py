from users.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 
            'street', 
            'number', 
            'complement', 
            'neighborhood', 
            'city', 
            'state', 
            'zip_code', 
            'is_primary'
        ]