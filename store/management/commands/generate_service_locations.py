import random
from store.models import ServiceLocation
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = 'Generate 10 random ServiceLocation objects'

    def handle(self, *args, **kwargs):
        fake = Faker()
        locations = []

        for _ in range(10):
            address = fake.address()[:10]
            locations.append(ServiceLocation(address=address))

        # Bulk create objects for better performance
        ServiceLocation.objects.bulk_create(locations)

        self.stdout.write(self.style.SUCCESS('Successfully generated 10 ServiceLocation objects'))
