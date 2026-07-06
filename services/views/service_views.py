from services.models import Service
from services.forms.service_form import ServiceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = '/services/'  # Redireciona para a lista de serviços após a criação

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)
    
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = '/services/'  # Redireciona para a lista de serviços após a atualização

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = '/services/'  # Redireciona para a lista de serviços após a exclusão