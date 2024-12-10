import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Card, ServiceLocation
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Generate fake data for the Card model'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of cards to generate")

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        users = CustomUser.objects.filter(is_active=True)
        locations = ServiceLocation.objects.all()

        if not users.exists() or not locations.exists():
            self.stdout.write(self.style.ERROR("You need at least one CustomUser and one ServiceLocation."))
            return

        cards = []
        for _ in range(count):
            card = Card(
                card_id=fake.uuid4(),
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                price=Decimal(fake.pydecimal(left_digits=5, right_digits=2, positive=True)),
                duration=random.randint(1, 15),
                provider=random.choice(users),
                is_active=fake.boolean(),
                is_feature=fake.boolean(),
                service_location=random.choice(locations),
            )
            cards.append(card)

        Card.objects.bulk_create(cards)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} Card objects.'))
