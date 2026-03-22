from django.urls import path
from . import views

urlpatterns = [
    path('wiki/', views.wiki_home, name='wiki_home'),
    path('wiki/search/', views.wiki_search, name='wiki_search'),
    path('wiki/type/<str:article_type>/', views.wiki_type, name='wiki_type'),
    path('wiki/category/<slug:slug>/', views.wiki_category, name='wiki_category'),
    path('wiki/<slug:slug>/', views.wiki_article, name='wiki_article'),
]
