from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'your@email.com', 'admin123')
            self.stdout.write('Superuser created!')
        else:
            self.stdout.write('Already exists.')