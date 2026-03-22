from django.core.management.base import BaseCommand
from reports.ml_trainer import train_models
from reports.ml_chatbot import train_chatbot, chatbot_model_exists


class Command(BaseCommand):
    help = 'Train the ML model and chatbot on synthetic medical data'

    def handle(self, *args, **options):
        self.stdout.write('Training report analysis ML model...')
        accuracy = train_models()
        self.stdout.write(self.style.SUCCESS(f'  Report ML model trained! Accuracy: {accuracy:.2%}'))

        self.stdout.write('Training MediBot TF-IDF chatbot...')
        train_chatbot()
        self.stdout.write(self.style.SUCCESS(f'  MediBot chatbot trained on Q&A knowledge base!'))

        self.stdout.write(self.style.SUCCESS('\nAll ML models ready!'))
