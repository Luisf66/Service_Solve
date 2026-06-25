from django.db import models


# Model para Mensagem
class Message(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField(help_text="Conteúdo da mensagem")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.sender} no serviço #{self.service.pk}"