from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Address, Telephone


# ============================================================
# Helpers
# ============================================================

def make_user(username='testuser', password='testpass123', user_type='client', **kwargs):
    return User.objects.create_user(
        username=username,
        password=password,
        user_type=user_type,
        **kwargs
    )


def make_address(user, **kwargs):
    defaults = {
        'street': 'Rua das Flores',
        'number': '123',
        'neighborhood': 'Centro',
        'city': 'Natal',
        'state': 'RN',
        'zip_code': '59000-000',
    }
    defaults.update(kwargs)
    return Address.objects.create(user=user, **defaults)


def make_telephone(user, number='84999999999', **kwargs):
    return Telephone.objects.create(user=user, number=number, **kwargs)

# ============================================================
# Views: User (HTML)
# ============================================================

class UserViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_user(username='viewuser', password='testpass123')
        self.client.login(username='viewuser', password='testpass123')

    def test_user_list_retorna_200(self):
        response = self.client.get(reverse('users:user_list'))
        self.assertEqual(response.status_code, 200)

    def test_user_list_template(self):
        response = self.client.get(reverse('users:user_list'))
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_user_list_contem_usuario(self):
        response = self.client.get(reverse('users:user_list'))
        self.assertContains(response, 'viewuser')

    def test_user_detail_retorna_200(self):
        response = self.client.get(reverse('users:user_detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_detail_template(self):
        response = self.client.get(reverse('users:user_detail', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(response, 'users/user_detail.html')

    def test_user_detail_404_inexistente(self):
        response = self.client.get(reverse('users:user_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_user_delete_retorna_200(self):
        response = self.client.get(reverse('users:user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_delete_post(self):
        user_to_delete = make_user(username='todelete', password='testpass123')
        response = self.client.post(reverse('users:user_delete', kwargs={'pk': user_to_delete.pk}))
        self.assertRedirects(response, reverse('users:user_list'))
        self.assertFalse(User.objects.filter(pk=user_to_delete.pk).exists())


# ============================================================
# Views: Address (HTML)
# ============================================================

class AddressViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_user(username='addruser', password='testpass123')
        self.client.login(username='addruser', password='testpass123')

    def test_address_create_get_retorna_200(self):
        response = self.client.get(
            reverse('users:user_address_create', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_address_create_post_cria_endereco(self):
        response = self.client.post(
            reverse('users:user_address_create', kwargs={'pk': self.user.pk}),
            {
                'street': 'Av. Brasil',
                'number': '500',
                'neighborhood': 'Tirol',
                'city': 'Natal',
                'state': 'RN',
                'zip_code': '59020-000',
                'is_primary': False,
            }
        )
        self.assertEqual(Address.objects.filter(user=self.user).count(), 1)

    def test_address_update_get_retorna_200(self):
        address = make_address(self.user)
        response = self.client.get(
            reverse('users:user_address_update', kwargs={'pk': self.user.pk, 'address_pk': address.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_address_delete_post_remove_endereco(self):
        address = make_address(self.user)
        self.client.post(
            reverse('users:user_address_delete', kwargs={'pk': self.user.pk, 'address_pk': address.pk})
        )
        self.assertFalse(Address.objects.filter(pk=address.pk).exists())


# ============================================================
# Views: Telephone (HTML)
# ============================================================

class TelephoneViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_user(username='teluser', password='testpass123')
        self.client.login(username='teluser', password='testpass123')

    def test_telephone_create_get_retorna_200(self):
        response = self.client.get(
            reverse('users:user_telephone_create', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_telephone_create_post_cria_telefone(self):
        self.client.post(
            reverse('users:user_telephone_create', kwargs={'pk': self.user.pk}),
            {'number': '84911111111', 'is_primary': False}
        )
        self.assertEqual(Telephone.objects.filter(user=self.user).count(), 1)

    def test_telephone_update_get_retorna_200(self):
        tel = make_telephone(self.user)
        response = self.client.get(
            reverse('users:user_telephone_update', kwargs={'pk': self.user.pk, 'telephone_pk': tel.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_telephone_delete_post_remove_telefone(self):
        tel = make_telephone(self.user)
        self.client.post(
            reverse('users:user_telephone_delete', kwargs={'pk': self.user.pk, 'telephone_pk': tel.pk})
        )
        self.assertFalse(Telephone.objects.filter(pk=tel.pk).exists())


# ============================================================
# Views: Auth
# ============================================================

class AuthViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_registro_get_retorna_200(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_registro_template(self):
        response = self.client.get(reverse('users:register'))
        self.assertTemplateUsed(response, 'auth/registration.html')

    def test_registro_cria_usuario(self):
        self.client.post(reverse('users:register'), {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password1': 'SenhaForte@123',
            'password2': 'SenhaForte@123',
            'user_type': 'client',
        })
        self.assertTrue(User.objects.filter(username='novousuario').exists())


    def test_registro_redireciona_apos_sucesso(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'novousuario2',
            'email': 'novo2@email.com',
            'password1': 'SenhaForte@123',
            'password2': 'SenhaForte@123',
            'user_type': 'client',
        })
        self.assertRedirects(response, reverse('login'))


# ============================================================
# API: User
# ============================================================

class UserAPITest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = make_user(username='apiuser', password='testpass123')
        refresh = RefreshToken.for_user(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_user_list_autenticado_retorna_200(self):
        response = self.api_client.get(reverse('users:user_api_list'))
        self.assertEqual(response.status_code, 200)

    def test_user_list_sem_autenticacao_retorna_401(self):
        client = APIClient()
        response = client.get(reverse('users:user_api_list'))
        self.assertEqual(response.status_code, 401)

    def test_user_list_retorna_usuarios(self):
        response = self.api_client.get(reverse('users:user_api_list'))
        self.assertGreaterEqual(len(response.data), 1)

    def test_user_detail_autenticado_retorna_200(self):
        response = self.api_client.get(
            reverse('users:user_api_detail', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_detail_retorna_dados_corretos(self):
        response = self.api_client.get(
            reverse('users:user_api_detail', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.data['username'], 'apiuser')

    def test_user_detail_sem_autenticacao_retorna_401(self):
        client = APIClient()
        response = client.get(
            reverse('users:user_api_detail', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 401)

    def test_user_detail_inexistente_retorna_404(self):
        response = self.api_client.get(
            reverse('users:user_api_detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)