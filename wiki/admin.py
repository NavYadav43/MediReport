from django.contrib import admin
from .models import WikiArticle, WikiCategory

@admin.register(WikiCategory)
class WikiCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(WikiArticle)
class WikiArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'article_type', 'category', 'is_featured', 'created_at']
    list_filter = ['article_type', 'category', 'is_featured']
    search_fields = ['title', 'overview', 'tags']
    prepopulated_fields = {'slug': ('title',)}
