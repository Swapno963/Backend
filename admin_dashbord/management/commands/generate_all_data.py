from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import IntegrityError

class Command(BaseCommand):
    help = "Generate all fake data in the correct sequence with error handling"

    def add_arguments(self, parser):
        parser.add_argument('user_count', type=int, help="Number of CustomUser to generate")
        parser.add_argument('card_count', type=int, help="Number of Cards to generate")
        parser.add_argument('menu_count', type=int, help="Number of Menus to generate")
        parser.add_argument('order_count', type=int, help="Number of Orders to generate")
        parser.add_argument('payment_count', type=int, help="Number of Payments to generate")

    def handle(self, *args, **kwargs):
        try:
            # Step 1: Generate CustomUser data
            user_count = kwargs['user_count']
            self.stdout.write(self.style.SUCCESS(f"Generating {user_count} CustomUsers..."))
            call_command('generate_custom_users', user_count)

            # Step 2: Generate Service location data
            self.stdout.write(self.style.SUCCESS(f"Generating Service locations..."))
            call_command('generate_service_locations')

            # Step 3: Generate Card data
            card_count = kwargs['card_count']
            self.stdout.write(self.style.SUCCESS(f"Generating {card_count} Cards..."))
            call_command('generate_cards', card_count)

            # Step 4: Generate Menu data
            menu_count = kwargs['menu_count']
            self.stdout.write(self.style.SUCCESS(f"Generating {menu_count} Menu..."))
            call_command('generate_menus', menu_count)

            # Step 5: Generate Order data
            order_count = kwargs['order_count']
            self.stdout.write(self.style.SUCCESS(f"Generating {order_count} Orders..."))
            call_command('generate_orders', order_count)

            # Step 6: Generate Payment data
            payment_count = kwargs['payment_count']
            self.stdout.write(self.style.SUCCESS(f"Generating {payment_count} Payments..."))
            call_command('generate_payments', payment_count)

            self.stdout.write(self.style.SUCCESS("Successfully generated all data in sequence!"))

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"IntegrityError: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
