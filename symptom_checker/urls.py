from django.urls import path
from . import views

urlpatterns = [
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
    path('api/analyze-symptoms/', views.analyze_api, name='analyze_symptoms'),
]
