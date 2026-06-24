from django.db import models


# Model para Review
class Review(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(help_text="Nota da avaliação (1 a 5)")
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'reviewer')  # cada usuário avalia uma vez por serviço

    def __str__(self):
        return f"Avaliação de {self.reviewer} para {self.reviewee} - {self.rating}★"