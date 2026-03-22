from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import WikiArticle, WikiCategory


def wiki_home(request):
    categories = WikiCategory.objects.all()
    featured = WikiArticle.objects.filter(is_featured=True)[:6]
    total_articles = WikiArticle.objects.count()
    diseases = WikiArticle.objects.filter(article_type='disease').count()
    terms = WikiArticle.objects.filter(article_type='term').count()
    drugs = WikiArticle.objects.filter(article_type='drug').count()
    return render(request, 'wiki/wiki_home.html', {
        'categories': categories, 'featured': featured,
        'total_articles': total_articles, 'diseases': diseases,
        'terms': terms, 'drugs': drugs,
    })


def wiki_category(request, slug):
    category = get_object_or_404(WikiCategory, slug=slug)
    articles = WikiArticle.objects.filter(category=category)
    return render(request, 'wiki/wiki_category.html', {'category': category, 'articles': articles})


def wiki_article(request, slug):
    article = get_object_or_404(WikiArticle, slug=slug)
    related = WikiArticle.objects.filter(category=article.category).exclude(pk=article.pk)[:4]
    return render(request, 'wiki/wiki_article.html', {'article': article, 'related': related})


def wiki_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = WikiArticle.objects.filter(
            Q(title__icontains=query) | Q(overview__icontains=query) |
            Q(symptoms__icontains=query) | Q(tags__icontains=query) |
            Q(treatments__icontains=query)
        )
    return render(request, 'wiki/wiki_search.html', {'query': query, 'results': results})


def wiki_type(request, article_type):
    type_labels = {'disease': 'Diseases & Conditions', 'term': 'Medical Terms', 'drug': 'Drugs & Medications'}
    articles = WikiArticle.objects.filter(article_type=article_type)
    return render(request, 'wiki/wiki_type.html', {
        'articles': articles,
        'type_label': type_labels.get(article_type, article_type.title()),
        'article_type': article_type,
    })
