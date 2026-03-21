from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_report, name='upload_report'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/<int:pk>/delete/', views.delete_report, name='delete_report'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('profile/', views.profile, name='profile'),
    path('manual-entry/', views.manual_entry, name='manual_entry'),
]
