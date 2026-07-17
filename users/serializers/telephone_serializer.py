from users.models import Telephone
from rest_framework import serializers


class TelephoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telephone
        fields = [
            'id',
            'number',
            'is_primary'
        ]