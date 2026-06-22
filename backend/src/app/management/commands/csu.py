from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=settings.ADMIN_EMAIL).exists():
            user = User.objects.create(username=settings.ADMIN_EMAIL)
            user.set_password(settings.ADMIN_PASSWORD)
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))
