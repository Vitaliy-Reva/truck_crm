from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Driver

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        today = timezone.localdate()

        drivers = Driver.objects.filter(
            status__in='W',
            weekend_until__lte=today
        )

        count = drivers.count()
        drivers.update(status='F', weekend_until=None)

        self.stdout.write(
            self.style.SUCCESS(f'Оновлено {count} водіїв → статус F')
        )