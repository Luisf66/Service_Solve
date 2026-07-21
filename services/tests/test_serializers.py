from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from services.models import Service, ServiceCategory
from services.serializers.service_serializer import ServiceSerializer
from services.serializers.category_serializer import ServiceCategorySerializer
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


def get_auth_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


# ============================================================
# Serializer: ServiceCategorySerializer
# ============================================================

class ServiceCategorySerializerTest(TestCase):

    def test_serializa_campos_corretos(self):
        cat = make_category(name='Eletricista')
        serializer = ServiceCategorySerializer(cat)
        self.assertIn('name', serializer.data)
        self.assertIn('description', serializer.data)

    def test_valores_serializados(self):
        cat = make_category(name='Pintor')
        serializer = ServiceCategorySerializer(cat)
        self.assertEqual(serializer.data['name'], 'Pintor')


# ============================================================
# Serializer: ServiceSerializer
# ============================================================

class ServiceSerializerTest(TestCase):

    def setUp(self):
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.category)

    def test_serializa_campos_obrigatorios(self):
        serializer = ServiceSerializer(self.service)
        campos = ['id', 'description', 'status', 'price', 'payment_method',
                  'displacement_start', 'displacement_end', 'created_at',
                  'updated_at', 'client', 'provider', 'category']
        for campo in campos:
            self.assertIn(campo, serializer.data)

    def test_status_pendente_serializado(self):
        serializer = ServiceSerializer(self.service)
        self.assertEqual(serializer.data['status'], 'pending')

    def test_provider_null_serializado(self):
        serializer = ServiceSerializer(self.service)
        self.assertIsNone(serializer.data['provider'])

    def test_client_serializado(self):
        serializer = ServiceSerializer(self.service)
        self.assertIsNotNone(serializer.data['client'])

    def test_category_serializada(self):
        serializer = ServiceSerializer(self.service)
        self.assertEqual(serializer.data['category']['name'], 'Encanador')

    def test_datas_formato_correto(self):
        serializer = ServiceSerializer(self.service)
        # formato esperado: dd/mm/YYYY HH:MM:SS
        created_at = serializer.data['created_at']
        self.assertRegex(created_at, r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}')


# ============================================================
# API: ServiceListView e ServiceDetailView
# ============================================================

class ServiceAPITest(TestCase):

    def setUp(self):
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.category)
        self.api_client = get_auth_client(self.client_user)

    def test_service_list_autenticado_retorna_200(self):
        response = self.api_client.get(reverse('services:service_api_list'))
        self.assertEqual(response.status_code, 200)

    def test_service_list_sem_autenticacao_retorna_401(self):
        client = APIClient()
        response = client.get(reverse('services:service_api_list'))
        self.assertEqual(response.status_code, 401)

    def test_service_list_retorna_servicos(self):
        response = self.api_client.get(reverse('services:service_api_list'))
        self.assertGreaterEqual(len(response.data), 1)

    def test_service_detail_autenticado_retorna_200(self):
        response = self.api_client.get(
            reverse('services:service_api_detail', kwargs={'pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_service_detail_retorna_dados_corretos(self):
        response = self.api_client.get(
            reverse('services:service_api_detail', kwargs={'pk': self.service.pk})
        )
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['description'], 'Descrição do serviço de teste')

    def test_service_detail_sem_autenticacao_retorna_401(self):
        client = APIClient()
        response = client.get(
            reverse('services:service_api_detail', kwargs={'pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 401)

    def test_service_detail_inexistente_retorna_404(self):
        response = self.api_client.get(
            reverse('services:service_api_detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_service_list_provider_ve_todos(self):
        api_provider = get_auth_client(self.provider_user)
        outro_cliente = make_user(username='outro', user_type='client')
        make_service(outro_cliente, self.category)
        response = api_provider.get(reverse('services:service_api_list'))
        self.assertGreaterEqual(len(response.data), 2)