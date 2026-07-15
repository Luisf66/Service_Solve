from users.models import User
from services.models import Service, ServiceStatusHistory
from services.forms.service_form import ServiceForm, PaymentProviderForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
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
    template_name = 'service_form.html'
    success_url = '/services/'

    def get_form_class(self):
        service = self.get_object()
        user = self.request.user

        if service.client == user:
            return ServiceForm

        if user.user_type == 'provider':
            return PaymentProviderForm

        # Se o usuário não é nem o criador nem um prestador, bloqueia o acesso
        raise PermissionDenied

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = '/services/'  # Redireciona para a lista de serviços após a exclusão

def service_accept(request, pk):
    service = Service.objects.get(pk=pk)

    if request.method == 'POST' and service.status == 'pending':
        service.provider = request.user
        service.status = 'accepted'
        service.save()
        # Criar histórico de status
        ServiceStatusHistory.objects.create(service=service, previous_status='pending', new_status='accepted', changed_by=request.user)
        return redirect('services:service_detail', pk=pk)
    return render(request, 'service_detail.html', {'service': service})

def service_cancel(request, pk):
    service = get_object_or_404(Service, pk=pk)
    user = request.user

    if request.method != 'POST':
        return redirect('services:service_detail', pk=pk)

    if user.cancellations_month <= 0:
        # sem cancelamentos disponíveis
        return redirect('services:service_detail', pk=pk)

    status_cancelavel = service.status in ['accepted', 'scheduled']

    if not status_cancelavel:
        return redirect('services:service_detail', pk=pk)

    if user == service.provider:
        previous_status = service.status
        service.status = 'canceled_by_provider'
        service.save()

        ServiceStatusHistory.objects.create(
            service=service,
            previous_status=previous_status,
            new_status='canceled_by_provider',
            changed_by=user
        )

        user.cancellations_month -= 1
        user.save()

    elif user == service.client:
        previous_status = service.status
        service.status = 'canceled_by_client'
        service.save()

        ServiceStatusHistory.objects.create(
            service=service,
            previous_status=previous_status,
            new_status='canceled_by_client',
            changed_by=user
        )

        user.cancellations_month -= 1
        user.save()

    else:
        # usuário não é parte do serviço
        return redirect('services:service_detail', pk=pk)

    return redirect('services:service_detail', pk=pk)

def service_complete(request, pk):
    service = Service.objects.get(pk=pk)

    if request.method == 'POST' and service.status == 'in_progress' and service.client == request.user:
        service.status = 'completed'
        service.save()
        # Criar histórico de status
        ServiceStatusHistory.objects.create(service=service, previous_status='in_progress', new_status='completed', changed_by=request.user)
        return redirect('services:service_detail', pk=pk)
    return render(request, 'service_detail.html', {'service': service})