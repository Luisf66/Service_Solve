# tasks.py (Celery, por exemplo)
from django.utils import timezone
from services.models import Service

def update_service_statuses():
    now = timezone.now()

    Service.objects.filter(
        status='scheduled',
        displacement_start__lte=now,
        displacement_end__gt=now
    ).update(status='in_displacement')

    Service.objects.filter(
        status='in_displacement',
        displacement_end__lte=now
    ).update(status='in_progress')