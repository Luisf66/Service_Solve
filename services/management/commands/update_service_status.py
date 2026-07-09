# services/management/commands/update_service_statuses.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from services.models import Service

class Command(BaseCommand):
    help = "Atualiza status de serviços baseado no tempo"

    def handle(self, *args, **options):
        now = timezone.now()

        updated_disp = Service.objects.filter(
            status='scheduled',
            displacement_start__lte=now,
            displacement_end__gt=now
        ).update(status='in_displacement')

        updated_prog = Service.objects.filter(
            status__in=['scheduled', 'in_displacement'],
            displacement_end__lte=now
        ).update(status='in_progress')

        self.stdout.write(f"{updated_disp} em deslocamento, {updated_prog} em andamento")


"""
crontab -e
* * * * * cd /caminho/do/projeto && /caminho/venv/bin/python 
manage.py update_service_statuses >> /var/log/service_status.log 2>&1
"""