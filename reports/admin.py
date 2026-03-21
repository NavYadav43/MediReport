from django.contrib import admin
from .models import MedicalReport, ChatMessage

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'report_type', 'status', 'risk_level', 'uploaded_at']
    list_filter = ['status', 'risk_level', 'report_type']
    search_fields = ['title', 'user__username', 'patient_name']
    readonly_fields = ['uploaded_at', 'analyzed_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'report', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'message']
