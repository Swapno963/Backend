import random
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Menu, Card

class Command(BaseCommand):
    help = 'Generate fake data for the Menu model'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of cards to generate")

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        cards = Card.objects.all()

        menus = []
        for _ in range(count):  
            menu_name = fake.company()
            menu_description = fake.text(max_nb_chars=200)
            menu_image = fake.image_url()
            menu_id = fake.uuid4()

    
            # Create the menu object
            menu = Menu(
                name=menu_name,
                description=menu_description,
                menu_id=menu_id,
            )
            menus.append(menu)

        Menu.objects.bulk_create(menus)

        self.stdout.write(self.style.SUCCESS("Successfully generated 10 Menu objects with random cards."))
