import random
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Menu, Card

class Command(BaseCommand):
    help = 'Generate fake data for the Menu model'

    def handle(self, *args, **kwargs):
        fake = Faker()
        cards = Card.objects.all()

        if cards.count() < 15:
            self.stdout.write(self.style.ERROR("You need at least 15 Card objects to generate menus."))
            return

        menus = []
        for _ in range(10):  # Generate 10 menus
            menu_name = fake.company()
            menu_description = fake.text(max_nb_chars=200)
            menu_image = fake.image_url()
            menu_id = fake.uuid4()

            # Randomly choose 3, 7, or 15 cards
            card_count = random.choice([3, 7, 15])
            selected_cards = random.sample(list(cards), card_count)

            # Create the menu object
            menu = Menu(
                name=menu_name,
                description=menu_description,
                menu_id=menu_id,
            )
            menu.save()  # Save to get a menu ID for ManyToMany relation
            menu.cards.set(selected_cards)  # Set the cards for the menu
            menus.append(menu)

        self.stdout.write(self.style.SUCCESS("Successfully generated 10 Menu objects with random cards."))
