from django.forms import ModelForm
from django.core.exceptions import ValidationError
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

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('O preço não pode ser negativo.')
        return price
