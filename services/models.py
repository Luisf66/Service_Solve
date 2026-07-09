from django.db import models


# Model Categoria de Serviço
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, help_text="Nome da categoria (ex: Encanador, Eletricista)")
    description = models.TextField(blank=True, null=True, help_text="Descrição da categoria")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Model Serviço
class Service(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('accepted', 'Aceito'),
        ('scheduled', 'Agendado'), 
        ('in_displacement', 'Em deslocamento'),
        ('in_progress', 'Em andamento'),
        ('completed', 'Concluído'), 
        ('rated', 'Avaliado'), #
        ('canceled_by_client', 'Cancelado pelo cliente'),
        ('canceled_by_provider', 'Cancelado pelo prestador de serviço'),
    )

    client = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='services_as_client')
    provider = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='services_as_provider', null=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='services', null=True, blank=True)
    description = models.TextField(help_text="Descrição do serviço solicitado")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Valor combinado no chat")
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text="Método de pagamento combinado (ex: PIX, Dinheiro)")
    displacement_start = models.DateTimeField(null=True, blank=True, help_text="Início da janela de deslocamento")
    displacement_end = models.DateTimeField(null=True, blank=True, help_text="Fim da janela de deslocamento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Serviço #{self.pk} - {self.status}"
    
    def save(self, *args, **kwargs):
        if self.displacement_start and self.displacement_end and self.status == 'accepted':
            self.status = 'scheduled'
            ServiceStatusHistory.objects.create(service=self, previous_status='accepted', new_status='scheduled', changed_by=self.client)
        super().save(*args, **kwargs)
    
# Model Categoria do Prestador
class ProviderCategory(models.Model):
    provider = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='providers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('provider', 'category')  # evita duplicatas

    def __str__(self):
        return f"{self.provider} - {self.category}"
    
# Model Histórico de Serviço
class ServiceStatusHistory(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=20, choices=Service.STATUS_CHOICES, null=True, blank=True)
    new_status = models.CharField(max_length=20, choices=Service.STATUS_CHOICES)
    changed_by = models.ForeignKey('users.User', on_delete=models.PROTECT)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Serviço #{self.service.pk}: {self.previous_status} → {self.new_status}"
