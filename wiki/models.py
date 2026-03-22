from django.db import models


class WikiCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default='📋')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Wiki Categories'

    def __str__(self):
        return self.name


class WikiArticle(models.Model):
    ARTICLE_TYPES = [
        ('disease', 'Disease / Condition'),
        ('term', 'Medical Term'),
        ('drug', 'Drug / Medication'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPES, default='disease')
    category = models.ForeignKey(WikiCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    icon = models.CharField(max_length=10, default='📋')
    overview = models.TextField()
    symptoms = models.TextField(blank=True)
    causes = models.TextField(blank=True)
    risk_factors = models.TextField(blank=True)
    treatments = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    prevention = models.TextField(blank=True)
    lifestyle_tips = models.TextField(blank=True)
    when_to_see_doctor = models.TextField(blank=True)
    related_tests = models.TextField(blank=True)
    tags = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]
