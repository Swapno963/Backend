import random
from store.models import ServiceLocation
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = 'Generate random ServiceLocation objects'


    def handle(self, *args, **kwargs):

        locations = ['Farmgate','Mirpur 1', 'Mirpur 10', 'Danmondi 32', 'khilkhet','Banani']

        service_location = []
        for lt in locations:
            location = ServiceLocation(
                address=lt
                )
            service_location.append(location)
        # Bulk create objects for better performance
        ServiceLocation.objects.bulk_create(service_location)

        self.stdout.write(self.style.SUCCESS('Successfully generated 10 ServiceLocation objects'))
