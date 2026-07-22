from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from services.forms.service_form import ServiceForm, PaymentProviderForm
from services.forms.category_form import ServiceCategoryForm
from services.models import ServiceCategory


# ============================================================
# Helpers
# ============================================================

def make_category(name='Encanador'):
    return ServiceCategory.objects.create(name=name)


# ============================================================
# Form: ServiceForm
# ============================================================

class ServiceFormTest(TestCase):

    def setUp(self):
        self.category = make_category()

    def test_form_valido_com_dados_corretos(self):
        form = ServiceForm(data={
            'description': 'Reparo de torneira',
            'category': self.category.pk,
            'payment_method': 'PIX',
        })
        self.assertTrue(form.is_valid())

    def test_form_valido_sem_category(self):
        form = ServiceForm(data={
            'description': 'Reparo de torneira',
            'category': '',
            'payment_method': 'PIX',
        })
        self.assertTrue(form.is_valid())

    def test_form_valido_sem_payment_method(self):
        form = ServiceForm(data={
            'description': 'Reparo de torneira',
            'category': self.category.pk,
            'payment_method': '',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_description(self):
        form = ServiceForm(data={
            'description': '',
            'category': self.category.pk,
            'payment_method': 'PIX',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_form_campos_corretos(self):
        form = ServiceForm()
        self.assertIn('description', form.fields)
        self.assertIn('category', form.fields)
        self.assertIn('payment_method', form.fields)


# ============================================================
# Form: PaymentProviderForm
# ============================================================

class PaymentProviderFormTest(TestCase):

    def test_form_valido_com_dados_corretos(self):
        inicio = timezone.now() + timedelta(hours=1)
        fim = timezone.now() + timedelta(hours=2)
        form = PaymentProviderForm(data={
            'price': '150.00',
            'displacement_start': inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'displacement_end': fim.strftime('%Y-%m-%d %H:%M:%S'),
        })
        self.assertTrue(form.is_valid())

    def test_form_valido_sem_displacement(self):
        form = PaymentProviderForm(data={
            'price': '200.00',
            'displacement_start': '',
            'displacement_end': '',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalido_price_negativo(self):
        form = PaymentProviderForm(data={
            'price': '-50.00',
            'displacement_start': '',
            'displacement_end': '',
        })
        self.assertFalse(form.is_valid())

    def test_form_campos_corretos(self):
        form = PaymentProviderForm()
        self.assertIn('price', form.fields)
        self.assertIn('displacement_start', form.fields)
        self.assertIn('displacement_end', form.fields)


# ============================================================
# Form: ServiceCategoryForm
# ============================================================

class ServiceCategoryFormTest(TestCase):

    def test_form_valido_com_nome(self):
        form = ServiceCategoryForm(data={
            'name': 'Eletricista',
            'description': 'Serviços elétricos',
        })
        self.assertTrue(form.is_valid())

    def test_form_valido_sem_description(self):
        form = ServiceCategoryForm(data={
            'name': 'Pintor',
            'description': '',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_nome(self):
        form = ServiceCategoryForm(data={
            'name': '',
            'description': 'Sem nome',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_campos_corretos(self):
        form = ServiceCategoryForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)