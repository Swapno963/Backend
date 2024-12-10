import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Card, ServiceLocation
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Generate fake data for the Card model'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = CustomUser.objects.filter(is_active=True)  # Assuming you want active users as providers
        locations = ServiceLocation.objects.all()

        if not users.exists() or not locations.exists():
            self.stdout.write(self.style.ERROR("You need at least one CustomUser and one ServiceLocation."))
            return

        cards = []
        for _ in range(10):  # Generate 10 cards
            card = Card(
                card_id=fake.uuid4(),
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                price=Decimal(fake.pydecimal(left_digits=5, right_digits=2, positive=True)),
                duration=random.randint(1, 365),  # Duration in days
                provider=random.choice(users),
                is_active=fake.boolean(),
                is_feature=fake.boolean(),
                service_location=random.choice(locations),
            )
            cards.append(card)

        Card.objects.bulk_create(cards)
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 Card objects.'))
