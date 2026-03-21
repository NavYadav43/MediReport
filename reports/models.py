from django.db import models
from django.contrib.auth.models import User

class MedicalReport(models.Model):
    REPORT_TYPES = [
        ('blood_test', 'Blood Test'),
        ('urine_test', 'Urine Test'),
        ('xray', 'X-Ray'),
        ('mri', 'MRI Scan'),
        ('ct_scan', 'CT Scan'),
        ('ecg', 'ECG/EKG'),
        ('lipid_profile', 'Lipid Profile'),
        ('thyroid', 'Thyroid Function'),
        ('liver_function', 'Liver Function'),
        ('kidney_function', 'Kidney Function'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('analyzing', 'Analyzing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES, default='other')
    file = models.FileField(upload_to='reports/%Y/%m/%d/')
    file_type = models.CharField(max_length=20, default='pdf')  # pdf, image
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analyzed_at = models.DateTimeField(null=True, blank=True)
    patient_name = models.CharField(max_length=255, blank=True)
    patient_age = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    # AI Analysis Results (stored as JSON text)
    analysis_summary = models.TextField(blank=True)
    key_findings = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    prevention = models.TextField(blank=True)
    lifestyle_advice = models.TextField(blank=True)
    when_to_see_doctor = models.TextField(blank=True)
    risk_level = models.CharField(max_length=20, blank=True)  # low, medium, high, critical
    raw_analysis = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    report = models.ForeignKey(MedicalReport, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Chat by {self.user.username} at {self.created_at}"
