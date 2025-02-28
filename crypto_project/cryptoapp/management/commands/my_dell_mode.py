from django.core.management.base import BaseCommand
from cryptoapp.models import ProfitPrice2, NumberData,dashbord_torgov




class Command(BaseCommand):
    help = 'My custom command'

    def handle(self, *args, **options):
        # while True:
            
            dashbord_torgov.objects.all().delete()

            # time.sleep(10)  # Подождите 10 секунд
# Удаляем все записи из модели YourModel
