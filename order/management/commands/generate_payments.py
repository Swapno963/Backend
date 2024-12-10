import random
from django.core.management.base import BaseCommand
from faker import Faker
from order.models import Payment, Order, CustomUser  

class Command(BaseCommand):
    help = "Generate fake Payment data"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of payments to generate")

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        # Fetch all existing orders and users to create relationships
        orders = Order.objects.all()
        users = CustomUser.objects.all()

        if not orders.exists() or not users.exists():
            self.stdout.write(self.style.ERROR("Please make sure there are Order and User objects in the database."))
            return

        payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']
        is_confirmed_choices = [True, False]

        for _ in range(count):
            # Randomly select order, customer, payment method, and confirmation status
            order = random.choice(orders)
            customer = random.choice(users)
            payment_method = random.choice(payment_methods)
            is_confirmed = random.choice(is_confirmed_choices)

            # Generate fake payment data
            payment = Payment.objects.create(
                email=fake.email(),
                payment_method=payment_method,
                sender_number=fake.phone_number()[:11],
                transaction_id=fake.phone_number()[:31],
                total_amount=random.randint(10, 50),
                order=order,
                customer=customer,
                is_confirmed=is_confirmed
            )

            self.stdout.write(self.style.SUCCESS(f"Payment {payment.transaction_id} created for Order {order.card_code}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} payments."))

