from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser('superadmin', 'itzzsiva05@gmail.com', 'super123')
            self.stdout.write('Superuser created!')
        else:
            self.stdout.write('Already exists.')
