from django.forms import ModelForm
from services.models import Service


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = [
            'description', 
            'category', 
            'payment_method',
        ]


class PaymentProviderForm(ModelForm):
    class Meta:
        model = Service
        fields = [
            'price',
            'displacement_start',
            'displacement_end',
        ]
