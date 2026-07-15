from django.db import models
from django.contrib.auth.models import AbstractUser


# Model Usuário
class User(AbstractUser):

    USER_TYPES = (
        ('client', 'Cliente'),
        ('provider', 'Prestador de Serviço'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client', help_text="Tipo de usuário")
    average_rating = models.FloatField(default=0, help_text="Avaliação média do usuário")
    total_ratings = models.IntegerField(default=0, help_text="Número total de avaliações do usuário")
    cancellations_month = models.IntegerField(default=3, help_text="Número de cancelamentos do usuário no mês")

    def __str__(self):
        return f'{self.username} - {self.user_type}'

# Model Endereço
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=150, help_text="Nome da rua do endereço do usuário")
    number = models.CharField(max_length=10, help_text="Número da residência do usuário")
    complement = models.CharField(max_length=100, blank=True, null=True, help_text="Complemento do endereço do usuário")
    neighborhood = models.CharField(max_length=150, help_text="Bairro do usuário")
    city = models.CharField(max_length=150, help_text="Cidade do usuário")
    state = models.CharField(max_length=2, help_text="Estado do usuário")
    zip_code = models.CharField(max_length=9, help_text="CEP do usuário")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.street}, {self.number} - {self.neighborhood}'

# Model Telefone
class Telephone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telephones')
    number = models.CharField(max_length=15, help_text="Número de telefone do usuário")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.number}'
    