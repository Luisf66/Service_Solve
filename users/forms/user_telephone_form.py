from users.models import User, Telephone
from django.forms import ModelForm


class TelephoneForm(ModelForm):
    class Meta:
        model = Telephone
        fields = ['number', 'is_primary']
        #widgets
        #labels