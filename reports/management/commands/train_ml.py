from django.core.management.base import BaseCommand
from reports.ml_trainer import train_models

class Command(BaseCommand):
    help = 'Train the ML model on synthetic medical data'

    def handle(self, *args, **options):
        self.stdout.write('Training ML model...')
        accuracy = train_models()
        self.stdout.write(self.style.SUCCESS(f'ML model trained successfully! Accuracy: {accuracy:.2%}'))
