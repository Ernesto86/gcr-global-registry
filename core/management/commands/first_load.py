from django.core.management import BaseCommand

from core.scripts.fill_default.fill_module import FillModule


class Command(BaseCommand):
    help = 'Load info initial system'

    def handle(self, *args, **options):
        FillModule().start()
