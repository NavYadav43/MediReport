from django.core.management.base import BaseCommand
from wiki.models import WikiCategory, WikiArticle
from wiki.knowledge_data import CATEGORIES, ARTICLES


class Command(BaseCommand):
    help = 'Load built-in medical wiki knowledge base'

    def handle(self, *args, **options):
        self.stdout.write('Loading wiki categories...')
        cat_map = {}
        for cat in CATEGORIES:
            obj, created = WikiCategory.objects.get_or_create(
                slug=cat['slug'],
                defaults={'name': cat['name'], 'icon': cat['icon'],
                          'order': cat['order'], 'description': cat['description']}
            )
            cat_map[cat['slug']] = obj
            if created:
                self.stdout.write(f'  Created category: {obj.name}')

        self.stdout.write('Loading wiki articles...')
        for art in ARTICLES:
            category = cat_map.get(art.get('category'))
            obj, created = WikiArticle.objects.get_or_create(
                slug=art['slug'],
                defaults={
                    'title': art['title'],
                    'article_type': art['type'],
                    'category': category,
                    'icon': art.get('icon', '📋'),
                    'overview': art.get('overview', ''),
                    'symptoms': art.get('symptoms', ''),
                    'causes': art.get('causes', ''),
                    'risk_factors': art.get('risk_factors', ''),
                    'treatments': art.get('treatments', ''),
                    'medications': art.get('medications', ''),
                    'prevention': art.get('prevention', ''),
                    'lifestyle_tips': art.get('lifestyle_tips', ''),
                    'when_to_see_doctor': art.get('when_to_see_doctor', ''),
                    'related_tests': art.get('related_tests', ''),
                    'tags': art.get('tags', ''),
                    'is_featured': art.get('featured', False),
                }
            )
            if created:
                self.stdout.write(f'  Created: {obj.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nWiki loaded! {WikiCategory.objects.count()} categories, {WikiArticle.objects.count()} articles.'
        ))
