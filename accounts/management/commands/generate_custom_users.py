import random
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser  

class Command(BaseCommand):
    help = "Generate fake CustomUser data"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of users to generate")

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        roles = ['super_admin', 'supplier', 'customer']

        for _ in range(count):
            name = fake.name()
            phone = fake.unique.phone_number()[:14]
            email = fake.unique.email()
            role = random.choice(roles)

            user = CustomUser.objects.create_user(
                name=name,
                phone=phone,
                email=email,
                role=role,
                password="12" 
            )
            self.stdout.write(self.style.SUCCESS(f"User {user.name} created with role {user.role}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} users."))
