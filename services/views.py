from services.models import Service
from services.forms.service_form import ServiceForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = '/services/'  # Redireciona para a lista de serviços após a criação