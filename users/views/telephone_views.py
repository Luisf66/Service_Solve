# users/views/telephone_views.py

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from users.models import Telephone, User
from users.forms.user_telephone_form import TelephoneForm


class TelephoneCreateView(CreateView):
    model = Telephone
    form_class = TelephoneForm
    template_name = 'telephones/telephone_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.kwargs['pk']   # pk vem da URL /users/<pk>/telephones/create/
        return context

    def form_valid(self, form):
        # garante que o telefone é vinculado ao usuário da URL
        form.instance.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.object.user.pk})


class TelephoneUpdateView(UpdateView):
    model = Telephone
    form_class = TelephoneForm
    template_name = 'telephones/telephone_form.html'
    pk_url_kwarg = 'telephone_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.object.user.pk
        return context

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.object.user.pk})


class TelephoneDeleteView(DeleteView):
    model = Telephone
    template_name = 'telephones/telephone_delete.html'
    pk_url_kwarg = 'telephone_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.object.user.pk
        return context

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.object.user.pk})