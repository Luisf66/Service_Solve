import json
from django.test import TestCase, Client
from django.urls import reverse
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

def make_message(service, sender, content='Olá!'):
    return Message.objects.create(service=service, sender=sender, content=content)


# ============================================================
# View: chat_detail
# ============================================================

class ChatDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.provider_user, self.category)

    def test_cliente_acessa_chat_retorna_200(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_provider_acessa_chat_retorna_200(self):
        self.client.login(username='prestador', password='testpass123')
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_terceiro_e_redirecionado(self):
        terceiro = make_user(username='terceiro', user_type='client')
        self.client.login(username='terceiro', password='testpass123')
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': self.service.pk})
        )
        self.assertRedirects(response, reverse('services:service_list'))

    def test_nao_autenticado_redireciona_para_login(self):
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_template_correto(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': self.service.pk})
        )
        self.assertTemplateUsed(response, 'chat_detail.html')

    def test_contexto_contem_service(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.context['service'], self.service)

    def test_contexto_contem_messages(self):
        make_message(self.service, self.client_user, 'Oi!')
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': self.service.pk})
        )
        self.assertIn('messages', response.context)
        self.assertEqual(response.context['messages'].count(), 1)

    def test_service_inexistente_retorna_404(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:chat_detail', kwargs={'service_pk': 99999})
        )
        self.assertEqual(response.status_code, 404)


# ============================================================
# View: message_list
# ============================================================

class MessageListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.provider_user, self.category)

    def test_retorna_200_e_json(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:message_list', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('messages', data)

    def test_retorna_mensagens_do_servico(self):
        make_message(self.service, self.client_user, 'Olá!')
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:message_list', kwargs={'service_pk': self.service.pk})
        )
        data = json.loads(response.content)
        self.assertEqual(len(data['messages']), 1)
        self.assertEqual(data['messages'][0]['content'], 'Olá!')

    def test_is_me_true_para_remetente_logado(self):
        make_message(self.service, self.client_user, 'Minha mensagem')
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:message_list', kwargs={'service_pk': self.service.pk})
        )
        data = json.loads(response.content)
        self.assertTrue(data['messages'][0]['is_me'])

    def test_is_me_false_para_outro_remetente(self):
        make_message(self.service, self.provider_user, 'Mensagem do prestador')
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:message_list', kwargs={'service_pk': self.service.pk})
        )
        data = json.loads(response.content)
        self.assertFalse(data['messages'][0]['is_me'])

    def test_polling_incremental_com_after(self):
        msg1 = make_message(self.service, self.client_user, 'Primeira')
        make_message(self.service, self.provider_user, 'Segunda')
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:message_list', kwargs={'service_pk': self.service.pk}),
            {'after': msg1.id}
        )
        data = json.loads(response.content)
        self.assertEqual(len(data['messages']), 1)
        self.assertEqual(data['messages'][0]['content'], 'Segunda')

    def test_terceiro_recebe_403(self):
        terceiro = make_user(username='terceiro', user_type='client')
        self.client.login(username='terceiro', password='testpass123')
        response = self.client.get(
            reverse('chat:message_list', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_nao_autenticado_redireciona(self):
        response = self.client.get(
            reverse('chat:message_list', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 302)


# ============================================================
# View: message_send
# ============================================================

class MessageSendViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client_user = make_user(username='cliente', user_type='client')
        self.provider_user = make_user(username='prestador', user_type='provider')
        self.category = make_category()
        self.service = make_service(self.client_user, self.provider_user, self.category)

    def test_envio_cria_mensagem(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': 'Nova mensagem'}
        )
        self.assertEqual(Message.objects.filter(service=self.service).count(), 1)

    def test_envio_retorna_json_com_dados(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': 'Mensagem teste'}
        )
        data = json.loads(response.content)
        self.assertEqual(data['content'], 'Mensagem teste')
        self.assertEqual(data['sender'], 'cliente')
        self.assertTrue(data['is_me'])

    def test_envio_retorna_201_ou_200(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': 'Mensagem teste'}
        )
        self.assertIn(response.status_code, [200, 201])

    def test_mensagem_vazia_retorna_400(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': '   '}
        )
        self.assertEqual(response.status_code, 400)

    def test_mensagem_vazia_nao_cria_registro(self):
        self.client.login(username='cliente', password='testpass123')
        self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': ''}
        )
        self.assertEqual(Message.objects.filter(service=self.service).count(), 0)

    def test_terceiro_recebe_403(self):
        terceiro = make_user(username='terceiro', user_type='client')
        self.client.login(username='terceiro', password='testpass123')
        response = self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': 'Tentativa'}
        )
        self.assertEqual(response.status_code, 403)

    def test_get_nao_permitido(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk})
        )
        self.assertEqual(response.status_code, 405)

    def test_nao_autenticado_redireciona(self):
        response = self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': 'Mensagem'}
        )
        self.assertEqual(response.status_code, 302)

    def test_provider_pode_enviar_mensagem(self):
        self.client.login(username='prestador', password='testpass123')
        self.client.post(
            reverse('chat:message_send', kwargs={'service_pk': self.service.pk}),
            {'content': 'Mensagem do prestador'}
        )
        msg = Message.objects.get(service=self.service)
        self.assertEqual(msg.sender, self.provider_user)