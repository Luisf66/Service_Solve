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
# Model: User
# ============================================================

class UserModelTest(TestCase):

    def test_criacao_usuario_client(self):
        user = make_user()
        self.assertEqual(user.user_type, 'client')
        self.assertEqual(user.average_rating, 0)
        self.assertEqual(user.total_ratings, 0)
        self.assertEqual(user.cancellations_month, 3)

    def test_criacao_usuario_provider(self):
        user = make_user(username='provider1', user_type='provider')
        self.assertEqual(user.user_type, 'provider')

    def test_str_usuario(self):
        user = make_user(username='joao')
        self.assertEqual(str(user), 'joao - client')

    def test_str_usuario_provider(self):
        user = make_user(username='carlos', user_type='provider')
        self.assertEqual(str(user), 'carlos - provider')

    def test_average_rating_default(self):
        user = make_user()
        self.assertEqual(user.average_rating, 0.0)

    def test_cancellations_month_default(self):
        user = make_user()
        self.assertEqual(user.cancellations_month, 3)

    def test_decremento_cancellations_month(self):
        user = make_user()
        user.cancellations_month -= 1
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.cancellations_month, 2)

    def test_atualizacao_average_rating(self):
        user = make_user()
        user.average_rating = 4.5
        user.total_ratings = 2
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.average_rating, 4.5)
        self.assertEqual(user.total_ratings, 2)


# ============================================================
# Model: Address
# ============================================================

class AddressModelTest(TestCase):

    def setUp(self):
        self.user = make_user()

    def test_criacao_endereco(self):
        address = make_address(self.user)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.city, 'Natal')
        self.assertEqual(address.state, 'RN')

    def test_str_endereco(self):
        address = make_address(self.user)
        self.assertEqual(str(address), 'Rua das Flores, 123 - Centro')

    def test_complement_opcional(self):
        address = make_address(self.user, complement=None)
        self.assertIsNone(address.complement)

    def test_is_primary_default_false(self):
        address = make_address(self.user)
        self.assertFalse(address.is_primary)

    def test_is_primary_true(self):
        address = make_address(self.user, is_primary=True)
        self.assertTrue(address.is_primary)

    def test_usuario_pode_ter_multiplos_enderecos(self):
        make_address(self.user, street='Rua A', number='1')
        make_address(self.user, street='Rua B', number='2')
        self.assertEqual(self.user.addresses.count(), 2)

    def test_deletar_usuario_deleta_enderecos(self):
        make_address(self.user)
        user_pk = self.user.pk
        self.user.delete()
        self.assertEqual(Address.objects.filter(user_id=user_pk).count(), 0)


# ============================================================
# Model: Telephone
# ============================================================

class TelephoneModelTest(TestCase):

    def setUp(self):
        self.user = make_user()

    def test_criacao_telefone(self):
        tel = make_telephone(self.user)
        self.assertEqual(tel.user, self.user)
        self.assertEqual(tel.number, '84999999999')

    def test_str_telefone(self):
        tel = make_telephone(self.user, number='84988888888')
        self.assertIn('84988888888', str(tel))

    def test_is_primary_default_false(self):
        tel = make_telephone(self.user)
        self.assertFalse(tel.is_primary)

    def test_usuario_pode_ter_multiplos_telefones(self):
        make_telephone(self.user, number='84999999991')
        make_telephone(self.user, number='84999999992')
        self.assertEqual(self.user.telephones.count(), 2)

    def test_deletar_usuario_deleta_telefones(self):
        make_telephone(self.user)
        user_pk = self.user.pk
        self.user.delete()
        self.assertEqual(Telephone.objects.filter(user_id=user_pk).count(), 0)
