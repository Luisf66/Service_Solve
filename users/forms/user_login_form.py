from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User

CSS_INPUT = 'w-full bg-zinc-800 border border-zinc-600 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-amber-500 transition-colors'

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': CSS_INPUT})
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': CSS_INPUT})
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={'class': CSS_INPUT})
    )

    class Meta:
        model = User
        fields = ('username', 'user_type', 'email', 'password1', 'password2')

        labels = {
            'user_type': 'Tipo de usuário',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': CSS_INPUT}),
            'user_type': forms.Select(attrs={'class': CSS_INPUT}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={'class': CSS_INPUT})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': CSS_INPUT})
    )