import csv
from django.core.management.base import BaseCommand
from cryptoapp.models import NumberData

class Command(BaseCommand):
    help = 'Export data from NumberData model to a CSV file'

    def handle(self, *args, **options):
        with open('numberdata.csv', 'w', newline='') as csvfile:
            field_names = [field.name for field in NumberData._meta.fields]
            writer = csv.writer(csvfile)
            writer.writerow(field_names)
            for obj in NumberData.objects.all():
                row = [getattr(obj, field) for field in field_names]
                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS('Data exported to numberdata.csv'))