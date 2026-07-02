# users/views/address_views.py

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from users.models import Address, User
from users.forms.user_address_form import AddressForm


class AddressListView(ListView):
    model = Address
    template_name = 'addresses/address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Address.objects.filter(user=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class AddressDetailView(DetailView):
    model = Address
    template_name = 'addresses/address_detail.html'
    context_object_name = 'address'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.object.user.pk
        return context


class AddressCreateView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'addresses/address_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.kwargs['pk']   # pk vem da URL /users/<pk>/addresses/create/
        return context

    def form_valid(self, form):
        # garante que o endereço é vinculado ao usuário da URL
        form.instance.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:user_addresses', kwargs={'pk': self.kwargs['pk']})


class AddressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'addresses/address_form.html'
    pk_url_kwarg = 'address_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.object.user.pk
        return context

    def get_success_url(self):
        return reverse('users:user_addresses', kwargs={'pk': self.object.user.pk})


class AddressDeleteView(DeleteView):
    model = Address
    template_name = 'addresses/address_delete.html'
    pk_url_kwarg = 'address_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.object.user.pk
        return context

    def get_success_url(self):
        return reverse('users:user_addresses', kwargs={'pk': self.object.user.pk})