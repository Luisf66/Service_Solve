from django.forms import ModelForm
from services.models import Service


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['description', 'category', 'provider', 'status', 'price', 'payment_method', 'displacement_start', 'displacement_end']