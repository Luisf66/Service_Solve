from services.models import Service
from services.forms.service_form import ServiceForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Service.objects.none()  # Retorna um queryset vazio se o usuário não estiver autenticado
        
        if self.request.user.user_type == 'provider':
            # Exibe todos os serviços
            return Service.objects.all()
        else:
            # Filtra os serviços para mostrar apenas os que pertencem ao usuário logado
            return Service.objects.filter(client=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Adiciona o usuário logado ao contexto
        return context

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

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Service.objects.none()  # Retorna um queryset vazio se o usuário não estiver autenticado
        
        if self.request.user.user_type == 'provider':
            # Exibe todos os serviços
            return Service.objects.all()
        else:
            # Filtra os serviços para mostrar apenas os que pertencem ao usuário logado
            return Service.objects.filter(client=self.request.user)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = '/services/'  # Redireciona para a lista de serviços após a atualização

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = '/services/'  # Redireciona para a lista de serviços após a exclusão

def service_accept(request, pk):
    service = Service.objects.get(pk=pk)

    print(f"Service Status: {service.status}\n")
    print(f"Service ID: {service.id}\n Service category: {service.category}\n Service description: {service.description}\n")
    print(f"Method: {request.method}\n")

    if request.method == 'POST':
        service.provider = request.user
        service.status = 'accepted'
        service.save()
        return redirect('services:service_detail', pk=pk)
    return render(request, 'service_detail.html', {'service': service})