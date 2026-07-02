from users.models import User, Address
from django.forms import ModelForm


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'complement', 'neighborhood', 'city', 'state', 'zip_code', 'is_primary']
        #widgets
        #labels