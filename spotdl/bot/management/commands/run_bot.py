from django.core.management.base import BaseCommand
from ...service import app


class Command(BaseCommand):
    help = 'runs telegram bot in a blocking mode'

    def handle(self, *args, **kwargs):
        app.run_polling()
