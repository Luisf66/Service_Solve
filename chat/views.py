from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from chat.models import Message
from services.models import Service


@login_required
def chat_detail(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)

    # só cliente e prestador do serviço podem acessar
    if request.user not in [service.client, service.provider]:
        return redirect('services:service_list')

    messages = service.messages.select_related('sender').order_by('sent_at')

    return render(request, 'chat_detail.html', {
        'service': service,
        'messages': messages,
    })


@login_required
def message_list(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)

    if request.user not in [service.client, service.provider]:
        return JsonResponse({'error': 'Acesso negado'}, status=403)

    # suporte a polling incremental — só retorna mensagens após determinado ID
    after_id = request.GET.get('after', 0)

    messages = service.messages.select_related('sender').filter(
        id__gt=after_id
    ).order_by('sent_at')

    data = [
        {
            'id': m.id,
            'sender': m.sender.username,
            'is_me': m.sender == request.user,
            'content': m.content,
            'sent_at': m.sent_at.strftime('%d/%m/%Y %H:%M'),
        }
        for m in messages
    ]

    return JsonResponse({'messages': data})


@login_required
@require_POST
def message_send(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)

    if request.user not in [service.client, service.provider]:
        return JsonResponse({'error': 'Acesso negado'}, status=403)

    content = request.POST.get('content', '').strip()

    if not content:
        return JsonResponse({'error': 'Mensagem vazia'}, status=400)

    message = Message.objects.create(
        service=service,
        sender=request.user,
        content=content,
    )

    return JsonResponse({
        'id': message.id,
        'sender': message.sender.username,
        'is_me': True,
        'content': message.content,
        'sent_at': message.sent_at.strftime('%d/%m/%Y %H:%M'),
    })