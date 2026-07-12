from django.forms import ModelForm
from services.models import ServiceCategory


class ServiceCategoryForm(ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name', 'description']