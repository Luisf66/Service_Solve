from django.test import TestCase
from chat.models import Message
from services.models import Service, ServiceCategory
from users.models import User


# ============================================================
# Helpers
# ============================================================

def make_user(username='testuser', password='testpass123', user_type='client', **kwargs):
    return User.objects.create_user(username=username, password=password, user_type=user_type, **kwargs)

def make_category(name='Encanador'):
    return ServiceCategory.objects.create(name=name)

def make_service(client, provider=None, category=None, status='accepted', **kwargs):
    return Service.objects.create(
        client=client, provider=provider, category=category,
        description='Serviço de teste', status=status, **kwargs
    )

def make_message(service, sender, content='Olá, tudo bem?'):
    return Message.objects.create(service=service, sender=sender, content=content)


# ============================================================
# Model: Message
# ============================================================

class MessageModelTest(TestCase):

    def setUp(self):
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.provider_user, self.category)

    def test_criacao_mensagem(self):
        msg = make_message(self.service, self.client_user)
        self.assertEqual(msg.service, self.service)
        self.assertEqual(msg.sender, self.client_user)
        self.assertEqual(msg.content, 'Olá, tudo bem?')

    def test_str_mensagem(self):
        msg = make_message(self.service, self.client_user)
        self.assertIn('cliente', str(msg))
        self.assertIn(str(self.service.pk), str(msg))

    def test_sent_at_preenchido_automaticamente(self):
        msg = make_message(self.service, self.client_user)
        self.assertIsNotNone(msg.sent_at)

    def test_multiplas_mensagens_por_servico(self):
        make_message(self.service, self.client_user, 'Primeira mensagem')
        make_message(self.service, self.provider_user, 'Segunda mensagem')
        make_message(self.service, self.client_user, 'Terceira mensagem')
        self.assertEqual(self.service.messages.count(), 3)

    def test_mensagens_ordenadas_por_sent_at(self):
        make_message(self.service, self.client_user, 'Primeira')
        make_message(self.service, self.provider_user, 'Segunda')
        msgs = list(self.service.messages.order_by('sent_at'))
        self.assertEqual(msgs[0].content, 'Primeira')
        self.assertEqual(msgs[1].content, 'Segunda')

    def test_deletar_service_deleta_mensagens(self):
        make_message(self.service, self.client_user)
        service_pk = self.service.pk
        self.service.delete()
        self.assertEqual(Message.objects.filter(service_id=service_pk).count(), 0)

    def test_messages_sent_do_sender(self):
        make_message(self.service, self.client_user)
        make_message(self.service, self.client_user, 'Segunda mensagem')
        self.assertEqual(self.client_user.messages_sent.count(), 2)

    def test_mensagem_vinculada_ao_service(self):
        msg = make_message(self.service, self.client_user)
        self.assertIn(msg, self.service.messages.all())