from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create moderators"

    def handle(self, *args, **options):
        moderators, created = Group.objects.get_or_create(name="moderators")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'moderators' успешно создана"))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "moderators" уже создана'))
