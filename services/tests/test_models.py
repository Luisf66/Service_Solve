from django.test import TestCase
from services.models import Service, ServiceCategory, ServiceStatusHistory, ProviderCategory
from users.models import User


# ============================================================
# Helpers
# ============================================================

def make_user(username='testuser', password='testpass123', user_type='client', **kwargs):
    return User.objects.create_user(username=username, password=password, user_type=user_type, **kwargs)


def make_category(name='Encanador', **kwargs):
    return ServiceCategory.objects.create(name=name, **kwargs)


def make_service(client, category=None, status='pending', **kwargs):
    return Service.objects.create(
        client=client,
        category=category,
        description='Descrição do serviço de teste',
        status=status,
        **kwargs
    )


# ============================================================
# Model: ServiceCategory
# ============================================================

class ServiceCategoryModelTest(TestCase):

    def test_criacao_categoria(self):
        cat = make_category()
        self.assertEqual(cat.name, 'Encanador')
        self.assertTrue(cat.is_active)

    def test_str_categoria(self):
        cat = make_category(name='Eletricista')
        self.assertEqual(str(cat), 'Eletricista')

    def test_is_active_default_true(self):
        cat = make_category()
        self.assertTrue(cat.is_active)

    def test_descricao_opcional(self):
        cat = make_category(description=None)
        self.assertIsNone(cat.description)

    def test_desativar_categoria(self):
        cat = make_category()
        cat.is_active = False
        cat.save()
        cat.refresh_from_db()
        self.assertFalse(cat.is_active)


# ============================================================
# Model: Service
# ============================================================

class ServiceModelTest(TestCase):

    def setUp(self):
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()

    def test_criacao_service(self):
        service = make_service(self.client_user, self.category)
        self.assertEqual(service.client, self.client_user)
        self.assertEqual(service.status, 'pending')
        self.assertIsNone(service.provider)

    def test_str_service(self):
        service = make_service(self.client_user)
        self.assertIn('Serviço #', str(service))
        self.assertIn('pending', str(service))

    def test_status_default_pending(self):
        service = make_service(self.client_user)
        self.assertEqual(service.status, 'pending')

    def test_provider_null_por_padrao(self):
        service = make_service(self.client_user)
        self.assertIsNone(service.provider)

    def test_price_null_por_padrao(self):
        service = make_service(self.client_user)
        self.assertIsNone(service.price)

    def test_payment_method_null_por_padrao(self):
        service = make_service(self.client_user)
        self.assertIsNone(service.payment_method)

    def test_atribuir_provider(self):
        service = make_service(self.client_user)
        service.provider = self.provider_user
        service.status = 'accepted'
        service.save()
        service.refresh_from_db()
        self.assertEqual(service.provider, self.provider_user)
        self.assertEqual(service.status, 'accepted')

    def test_todos_status_choices_validos(self):
        status_validos = [
            'pending', 'accepted', 'scheduled', 'in_displacement',
            'in_progress', 'completed', 'rated',
            'canceled_by_client', 'canceled_by_provider'
        ]
        service = make_service(self.client_user)
        for status in status_validos:
            service.status = status
            service.save()
            service.refresh_from_db()
            self.assertEqual(service.status, status)

    def test_save_muda_status_para_scheduled_com_janela(self):
        from django.utils import timezone
        from datetime import timedelta
        service = make_service(self.client_user, self.category, status='accepted')
        service.provider = self.provider_user
        service.displacement_start = timezone.now() + timedelta(hours=1)
        service.displacement_end = timezone.now() + timedelta(hours=2)
        service.save()
        service.refresh_from_db()
        self.assertEqual(service.status, 'scheduled')

    def test_created_at_preenchido_automaticamente(self):
        service = make_service(self.client_user)
        self.assertIsNotNone(service.created_at)

    def test_updated_at_preenchido_automaticamente(self):
        service = make_service(self.client_user)
        self.assertIsNotNone(service.updated_at)


# ============================================================
# Model: ProviderCategory
# ============================================================

class ProviderCategoryModelTest(TestCase):

    def setUp(self):
        self.provider = make_user(username='prov', user_type='provider')
        self.category = make_category()

    def test_criacao_provider_category(self):
        pc = ProviderCategory.objects.create(provider=self.provider, category=self.category)
        self.assertEqual(pc.provider, self.provider)
        self.assertEqual(pc.category, self.category)

    def test_str_provider_category(self):
        pc = ProviderCategory.objects.create(provider=self.provider, category=self.category)
        self.assertIn(str(self.provider), str(pc))
        self.assertIn(str(self.category), str(pc))

    def test_unique_together_impede_duplicata(self):
        from django.db import IntegrityError
        ProviderCategory.objects.create(provider=self.provider, category=self.category)
        with self.assertRaises(IntegrityError):
            ProviderCategory.objects.create(provider=self.provider, category=self.category)

    def test_provider_pode_ter_multiplas_categorias(self):
        cat2 = make_category(name='Eletricista')
        ProviderCategory.objects.create(provider=self.provider, category=self.category)
        ProviderCategory.objects.create(provider=self.provider, category=cat2)
        self.assertEqual(self.provider.categories.count(), 2)


# ============================================================
# Model: ServiceStatusHistory
# ============================================================

class ServiceStatusHistoryModelTest(TestCase):

    def setUp(self):
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.service = make_service(self.client_user)

    def test_criacao_historico(self):
        history = ServiceStatusHistory.objects.create(
            service=self.service,
            previous_status='pending',
            new_status='accepted',
            changed_by=self.provider_user
        )
        self.assertEqual(history.previous_status, 'pending')
        self.assertEqual(history.new_status, 'accepted')
        self.assertEqual(history.changed_by, self.provider_user)

    def test_str_historico(self):
        history = ServiceStatusHistory.objects.create(
            service=self.service,
            previous_status='pending',
            new_status='accepted',
            changed_by=self.provider_user
        )
        self.assertIn('pending', str(history))
        self.assertIn('accepted', str(history))

    def test_previous_status_pode_ser_null(self):
        history = ServiceStatusHistory.objects.create(
            service=self.service,
            previous_status=None,
            new_status='pending',
            changed_by=self.client_user
        )
        self.assertIsNone(history.previous_status)

    def test_changed_at_preenchido_automaticamente(self):
        history = ServiceStatusHistory.objects.create(
            service=self.service,
            previous_status='pending',
            new_status='accepted',
            changed_by=self.provider_user
        )
        self.assertIsNotNone(history.changed_at)

    def test_service_tem_multiplos_historicos(self):
        ServiceStatusHistory.objects.create(
            service=self.service, previous_status=None,
            new_status='pending', changed_by=self.client_user
        )
        ServiceStatusHistory.objects.create(
            service=self.service, previous_status='pending',
            new_status='accepted', changed_by=self.provider_user
        )
        self.assertEqual(self.service.status_history.count(), 2)

    def test_deletar_service_deleta_historico(self):
        ServiceStatusHistory.objects.create(
            service=self.service, previous_status='pending',
            new_status='accepted', changed_by=self.provider_user
        )
        service_pk = self.service.pk
        self.service.delete()
        self.assertEqual(ServiceStatusHistory.objects.filter(service_id=service_pk).count(), 0)