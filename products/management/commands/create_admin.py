import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create superuser safely from CLI arguments or environment variables'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default=None, help='Admin username')
        parser.add_argument('--email', type=str, default=None, help='Admin email')
        parser.add_argument('--password', type=str, default=None, help='Admin password')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username'] or os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = options['email'] or os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = options['password'] or os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))
            return

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    "Please provide password via --password or DJANGO_SUPERUSER_PASSWORD, "
                    "or run: python manage.py createsuperuser"
                )
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' was created successfully!"))

