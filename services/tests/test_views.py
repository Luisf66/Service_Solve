from django.test import TestCase, Client
from django.urls import reverse
from services.models import Service, ServiceCategory, ServiceStatusHistory
from users.models import User


# ============================================================
# Helpers
# ============================================================

def make_user(username='testuser', password='testpass123', user_type='client', **kwargs):
    return User.objects.create_user(username=username, password=password, user_type=user_type, **kwargs)


def make_category(name='Encanador'):
    return ServiceCategory.objects.create(name=name)


def make_service(client, category=None, status='pending', **kwargs):
    return Service.objects.create(
        client=client,
        category=category,
        description='Descrição do serviço de teste',
        status=status,
        **kwargs
    )


# ============================================================
# Views: ServiceCategory
# ============================================================

class ServiceCategoryViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_user(username='admin', user_type='client')
        self.client.login(username='admin', password='testpass123')
        self.category = make_category()

    def test_category_list_retorna_200(self):
        response = self.client.get(reverse('services:category_list'))
        self.assertEqual(response.status_code, 200)

    def test_category_list_template(self):
        response = self.client.get(reverse('services:category_list'))
        self.assertTemplateUsed(response, 'categories/category_list.html')

    def test_category_list_contem_categoria(self):
        response = self.client.get(reverse('services:category_list'))
        self.assertContains(response, 'Encanador')

    def test_category_create_get_retorna_200(self):
        response = self.client.get(reverse('services:category_create'))
        self.assertEqual(response.status_code, 200)

    def test_category_create_post_cria_categoria(self):
        self.client.post(reverse('services:category_create'), {
            'name': 'Pintor',
            'description': 'Serviços de pintura',
        })
        self.assertTrue(ServiceCategory.objects.filter(name='Pintor').exists())

    def test_category_update_get_retorna_200(self):
        response = self.client.get(
            reverse('services:category_update', kwargs={'pk': self.category.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_category_update_post_atualiza(self):
        self.client.post(
            reverse('services:category_update', kwargs={'pk': self.category.pk}),
            {'name': 'Encanador Atualizado', 'description': 'Nova descrição'}
        )
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Encanador Atualizado')

    def test_category_delete_get_retorna_200(self):
        response = self.client.get(
            reverse('services:category_delete', kwargs={'pk': self.category.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_category_delete_post_desativa_categoria(self):
        self.client.post(
            reverse('services:category_delete', kwargs={'pk': self.category.pk})
        )
        self.category.refresh_from_db()
        self.assertFalse(self.category.is_active)


# ============================================================
# Views: Service (CRUD)
# ============================================================

class ServiceCRUDViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.client.login(username='cliente', password='testpass123')
        self.service = make_service(self.client_user, self.category)

    def test_service_list_retorna_200(self):
        response = self.client.get(reverse('services:service_list'))
        self.assertEqual(response.status_code, 200)

    def test_service_list_template(self):
        response = self.client.get(reverse('services:service_list'))
        self.assertTemplateUsed(response, 'service_list.html')

    def test_service_list_cliente_ve_apenas_seus_servicos(self):
        outro_cliente = make_user(username='outro', user_type='client')
        make_service(outro_cliente, self.category)
        response = self.client.get(reverse('services:service_list'))
        for service in response.context['services']:
            self.assertEqual(service.client, self.client_user)

    def test_service_list_provider_ve_todos_servicos(self):
        self.client.login(username='prestador', password='testpass123')
        outro_cliente = make_user(username='outro', user_type='client')
        make_service(outro_cliente, self.category)
        response = self.client.get(reverse('services:service_list'))
        self.assertGreaterEqual(response.context['services'].count(), 2)

    def test_service_detail_retorna_200(self):
        response = self.client.get(
            reverse('services:service_detail', kwargs={'pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_service_detail_template(self):
        response = self.client.get(
            reverse('services:service_detail', kwargs={'pk': self.service.pk})
        )
        self.assertTemplateUsed(response, 'service_detail.html')

    def test_service_create_get_retorna_200(self):
        response = self.client.get(reverse('services:service_create'))
        self.assertEqual(response.status_code, 200)

    def test_service_create_post_cria_servico(self):
        self.client.post(reverse('services:service_create'), {
            'description': 'Novo serviço de teste',
            'category': self.category.pk,
            'payment_method': 'PIX',
        })
        self.assertTrue(
            Service.objects.filter(description='Novo serviço de teste').exists()
        )

    def test_service_create_vincula_cliente_logado(self):
        self.client.post(reverse('services:service_create'), {
            'description': 'Serviço do cliente logado',
            'category': self.category.pk,
            'payment_method': 'Dinheiro',
        })
        service = Service.objects.get(description='Serviço do cliente logado')
        self.assertEqual(service.client, self.client_user)

    def test_service_update_get_retorna_200(self):
        response = self.client.get(
            reverse('services:service_update', kwargs={'pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_service_delete_get_retorna_200(self):
        response = self.client.get(
            reverse('services:service_delete', kwargs={'pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_service_delete_post_remove_servico(self):
        service_to_delete = make_service(self.client_user, self.category)
        self.client.post(
            reverse('services:service_delete', kwargs={'pk': service_to_delete.pk})
        )
        self.assertFalse(Service.objects.filter(pk=service_to_delete.pk).exists())


# ============================================================
# Views: service_accept
# ============================================================

class ServiceAcceptViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.category, status='pending')

    def test_accept_por_provider_muda_status(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.post(reverse('services:service_accept', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'accepted')

    def test_accept_vincula_provider(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.post(reverse('services:service_accept', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.provider, self.provider_user)

    def test_accept_cria_historico(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.post(reverse('services:service_accept', kwargs={'pk': self.service.pk}))
        self.assertTrue(
            ServiceStatusHistory.objects.filter(
                service=self.service, new_status='accepted'
            ).exists()
        )

    def test_accept_nao_funciona_se_status_nao_for_pending(self):
        self.service.status = 'accepted'
        self.service.provider = self.provider_user
        self.service.save()
        outro_provider = make_user(username='outro_prov', user_type='provider')
        self.client.login(username='outro_prov', password='testpass123')
        self.client.post(reverse('services:service_accept', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.provider, self.provider_user)

    def test_accept_get_nao_muda_status(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.get(reverse('services:service_accept', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'pending')


# ============================================================
# Views: service_cancel
# ============================================================

class ServiceCancelViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.category, status='accepted')
        self.service.provider = self.provider_user
        self.service.save()

    def test_cliente_cancela_servico_accepted(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'canceled_by_client')

    def test_provider_cancela_servico_accepted(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.post(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'canceled_by_provider')

    def test_cancelamento_decrementa_cancellations_month(self):
        self.client.login(username='cliente', password='testpass123')
        cancelamentos_antes = self.client_user.cancellations_month
        self.client.post(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.client_user.refresh_from_db()
        self.assertEqual(self.client_user.cancellations_month, cancelamentos_antes - 1)

    def test_cancelamento_sem_creditos_nao_cancela(self):
        self.client_user.cancellations_month = 0
        self.client_user.save()
        self.client.login(username='cliente', password='testpass123')
        self.client.post(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'accepted')

    def test_cancelamento_cria_historico(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.assertTrue(
            ServiceStatusHistory.objects.filter(
                service=self.service, new_status='canceled_by_client'
            ).exists()
        )

    def test_cancelamento_status_invalido_nao_cancela(self):
        self.service.status = 'completed'
        self.service.save()
        self.client.login(username='cliente', password='testpass123')
        self.client.post(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'completed')

    def test_cancelamento_get_nao_cancela(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.get(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'accepted')

    def test_terceiro_nao_pode_cancelar(self):
        terceiro = make_user(username='terceiro', user_type='client')
        self.client.login(username='terceiro', password='testpass123')
        self.client.post(reverse('services:service_cancel', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'accepted')


# ============================================================
# Views: service_complete
# ============================================================

class ServiceCompleteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.category, status='in_progress')
        self.service.provider = self.provider_user
        self.service.save()

    def test_cliente_completa_servico(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(reverse('services:service_complete', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'completed')

    def test_complete_cria_historico(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(reverse('services:service_complete', kwargs={'pk': self.service.pk}))
        self.assertTrue(
            ServiceStatusHistory.objects.filter(
                service=self.service, new_status='completed'
            ).exists()
        )

    def test_provider_nao_pode_completar(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.post(reverse('services:service_complete', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'in_progress')

    def test_complete_status_invalido_nao_completa(self):
        self.service.status = 'accepted'
        self.service.save()
        self.client.login(username='cliente', password='testpass123')
        self.client.post(reverse('services:service_complete', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'accepted')

    def test_complete_get_nao_muda_status(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.get(reverse('services:service_complete', kwargs={'pk': self.service.pk}))
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, 'in_progress')