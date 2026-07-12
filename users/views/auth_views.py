from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms.user_form import UserForm
from users.forms.user_login_form import RegistroForm


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'auth/registration.html'
    success_url = reverse_lazy('login')

@login_required
def perfil_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('services:services_list')
    else:
        form = UserForm(instance=request.user)

    return render(request, 'perfil.html', {'form': form})