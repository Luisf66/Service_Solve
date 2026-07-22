from django.test import TestCase
from django.db import IntegrityError
from reviews.models import Review
from services.models import Service, ServiceCategory
from users.models import User


# ============================================================
# Helpers
# ============================================================

def make_user(username='testuser', password='testpass123', user_type='client', **kwargs):
    return User.objects.create_user(username=username, password=password, user_type=user_type, **kwargs)

def make_category(name='Encanador'):
    return ServiceCategory.objects.create(name=name)

def make_service(client, provider=None, category=None, status='completed', **kwargs):
    return Service.objects.create(
        client=client, provider=provider, category=category,
        description='Descrição do serviço de teste', status=status, **kwargs
    )

def make_review(service, reviewer, reviewee, rating=5, comment='Ótimo serviço'):
    return Review.objects.create(
        service=service, reviewer=reviewer, reviewee=reviewee,
        rating=rating, comment=comment,
    )


# ============================================================
# Model: Review
# ============================================================

class ReviewModelTest(TestCase):

    def setUp(self):
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.provider_user, self.category)

    def test_criacao_review(self):
        review = make_review(self.service, self.client_user, self.provider_user)
        self.assertEqual(review.service, self.service)
        self.assertEqual(review.reviewer, self.client_user)
        self.assertEqual(review.reviewee, self.provider_user)
        self.assertEqual(review.rating, 5)

    def test_str_review(self):
        review = make_review(self.service, self.client_user, self.provider_user, rating=4)
        self.assertIn('cliente', str(review))
        self.assertIn('prestador', str(review))
        self.assertIn('4★', str(review))

    def test_comment_opcional(self):
        review = make_review(self.service, self.client_user, self.provider_user, comment=None)
        self.assertIsNone(review.comment)

    def test_created_at_preenchido_automaticamente(self):
        review = make_review(self.service, self.client_user, self.provider_user)
        self.assertIsNotNone(review.created_at)

    def test_unique_together_impede_avaliacao_duplicada(self):
        make_review(self.service, self.client_user, self.provider_user)
        with self.assertRaises(IntegrityError):
            make_review(self.service, self.client_user, self.provider_user, rating=1)

    def test_duas_avaliacoes_por_servico(self):
        make_review(self.service, self.client_user, self.provider_user, rating=5)
        make_review(self.service, self.provider_user, self.client_user, rating=4)
        self.assertEqual(self.service.reviews.count(), 2)

    def test_deletar_service_deleta_reviews(self):
        make_review(self.service, self.client_user, self.provider_user)
        service_pk = self.service.pk
        self.service.delete()
        self.assertEqual(Review.objects.filter(service_id=service_pk).count(), 0)

    def test_reviews_given_do_reviewer(self):
        make_review(self.service, self.client_user, self.provider_user)
        self.assertEqual(self.client_user.reviews_given.count(), 1)

    def test_reviews_received_do_reviewee(self):
        make_review(self.service, self.client_user, self.provider_user)
        self.assertEqual(self.provider_user.reviews_received.count(), 1)