import random
from django.core.management.base import BaseCommand
from faker import Faker
from order.models import Order, CustomUser, Card 

class Command(BaseCommand):
    help = "Generate fake Order data"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of orders to generate")

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        # Fetch all existing cards and users to create relationships
        cards = Card.objects.all()
        users = CustomUser.objects.all()

        if not cards.exists() or not users.exists():
            self.stdout.write(self.style.ERROR("Please make sure there are Card and User objects in the database."))
            return

        order_status_choices = [Order.PENDING, Order.ACCEPTED, Order.DELIVERED]

        for _ in range(count):
            # Randomly select card, customer, and status
            card = random.choice(cards)
            customer = random.choice(users)
            status = random.choice(order_status_choices)

            # Create order with random delivery date, status, and payment status
            order = Order.objects.create(
                card_code=fake.unique.lexify(text="???"),
                delivery_date=fake.date_time_this_year(),
                status=status,
                is_paid=fake.boolean(),
                card=card,
                customer=customer,
            )

            self.stdout.write(self.style.SUCCESS(f"Order {order.card_code} created for {order.customer.name} with status {order.status}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} orders."))

