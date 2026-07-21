from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Avg
from reviews.models import Review
from services.models import Service, ServiceCategory, ServiceStatusHistory
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


# ============================================================
# View: service_review
# ============================================================

class ServiceReviewViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(
            self.client_user, self.provider_user, self.category, status='completed'
        )

    def test_get_retorna_200(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_usa_template_correto(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk})
        )
        self.assertTemplateUsed(response, 'review_create.html')

    def test_cliente_avalia_prestador(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 5, 'comment': 'Ótimo profissional!'}
        )
        review = Review.objects.get(service=self.service, reviewer=self.client_user)
        self.assertEqual(review.reviewee, self.provider_user)
        self.assertEqual(review.rating, 5)

    def test_prestador_avalia_cliente(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 4, 'comment': 'Cliente atencioso'}
        )
        review = Review.objects.get(service=self.service, reviewer=self.provider_user)
        self.assertEqual(review.reviewee, self.client_user)
        self.assertEqual(review.rating, 4)

    def test_avaliacao_muda_status_para_rated(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 5, 'comment': 'Perfeito!'}
        )
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'rated')

    def test_avaliacao_cria_historico_de_status(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 5, 'comment': 'Perfeito!'}
        )
        self.assertTrue(
            ServiceStatusHistory.objects.filter(
                service=self.service, new_status='rated'
            ).exists()
        )

    def test_avaliacao_incrementa_total_ratings_do_avaliado(self):
        total_antes = self.provider_user.total_ratings
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 5, 'comment': 'Ótimo!'}
        )
        self.provider_user.refresh_from_db()
        self.assertEqual(self.provider_user.total_ratings, total_antes + 1)

    def test_avaliacao_atualiza_average_rating_do_avaliado(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 4, 'comment': 'Bom serviço'}
        )
        self.provider_user.refresh_from_db()
        self.assertEqual(self.provider_user.average_rating, 4.0)

    def test_avaliacao_redireciona_para_service_detail(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 5, 'comment': 'Excelente!'}
        )
        self.assertRedirects(
            response,
            reverse('services:service_detail', kwargs={'pk': self.service.pk})
        )

    def test_form_invalido_nao_cria_review(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': '', 'comment': 'Sem nota'}
        )
        self.assertEqual(Review.objects.filter(service=self.service).count(), 0)

    def test_service_inexistente_retorna_404(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('reviews:review_create', kwargs={'service_pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_average_rating_com_multiplas_avaliacoes(self):
        # cria um segundo serviço para o mesmo provider
        service2 = make_service(
            self.client_user, self.provider_user, self.category, status='completed'
        )
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': self.service.pk}),
            {'rating': 4, 'comment': 'Bom'}
        )
        self.service.status = 'completed'
        self.service.save()
        self.client.post(
            reverse('reviews:review_create', kwargs={'service_pk': service2.pk}),
            {'rating': 2, 'comment': 'Regular'}
        )
        self.provider_user.refresh_from_db()
        expected_avg = round((4 + 2) / 2, 2)
        self.assertEqual(self.provider_user.average_rating, expected_avg)