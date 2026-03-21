import json
import os
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import MedicalReport, ChatMessage
from .gemini_service import analyze_medical_report, chat_with_ai


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1,
                                            first_name=first_name, last_name=last_name)
            login(request, user)
            messages.success(request, f'Welcome to MediReport, {first_name or username}!')
            return redirect('dashboard')
    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    reports = MedicalReport.objects.filter(user=request.user)
    context = {
        'recent_reports': reports[:5],
        'total_reports': reports.count(),
        'completed_reports': reports.filter(status='completed').count(),
        'pending_reports': reports.filter(status__in=['pending', 'analyzing']).count(),
        'high_risk_reports': reports.filter(risk_level__in=['high', 'critical']).count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def upload_report(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        report_type = request.POST.get('report_type', 'other')
        patient_name = request.POST.get('patient_name', '').strip()
        patient_age = request.POST.get('patient_age', '')
        notes = request.POST.get('notes', '').strip()
        file = request.FILES.get('file')
        if not title or not file:
            messages.error(request, 'Title and file are required.')
            return render(request, 'upload.html', {'report_types': MedicalReport.REPORT_TYPES})
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'webp']
        file_ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
        if file_ext not in allowed_extensions:
            messages.error(request, 'Only PDF, JPG, PNG, and WEBP files are allowed.')
            return render(request, 'upload.html', {'report_types': MedicalReport.REPORT_TYPES})
        if file.size > 10 * 1024 * 1024:
            messages.error(request, 'File size must be less than 10MB.')
            return render(request, 'upload.html', {'report_types': MedicalReport.REPORT_TYPES})
        report = MedicalReport.objects.create(
            user=request.user, title=title, report_type=report_type,
            file=file, file_type=file_ext, patient_name=patient_name,
            patient_age=int(patient_age) if patient_age.isdigit() else None,
            notes=notes, status='analyzing'
        )
        analysis = analyze_medical_report(report.file.path, file_ext, report_type)
        if 'error' not in analysis:
            report.analysis_summary = analysis.get('summary', '')
            report.key_findings = json.dumps(analysis.get('key_findings', []))
            report.medications = json.dumps(analysis.get('medications', []))
            report.precautions = json.dumps(analysis.get('precautions', []))
            report.prevention = json.dumps(analysis.get('prevention', []))
            report.lifestyle_advice = json.dumps(analysis.get('lifestyle_advice', []))
            report.when_to_see_doctor = json.dumps(analysis.get('when_to_see_doctor', []))
            report.risk_level = analysis.get('risk_level', 'low')
            report.raw_analysis = json.dumps(analysis)
            report.status = 'completed'
            report.analyzed_at = datetime.now()
        else:
            report.analysis_summary = f"Analysis note: {analysis.get('error', 'Unknown error')}"
            report.status = 'failed'
        report.save()
        messages.success(request, 'Report uploaded and analyzed!')
        return redirect('report_detail', pk=report.pk)
    return render(request, 'upload.html', {'report_types': MedicalReport.REPORT_TYPES})


@login_required
def report_list(request):
    reports = MedicalReport.objects.filter(user=request.user)
    filter_type = request.GET.get('type', '')
    filter_status = request.GET.get('status', '')
    if filter_type:
        reports = reports.filter(report_type=filter_type)
    if filter_status:
        reports = reports.filter(status=filter_status)
    return render(request, 'report_list.html', {
        'reports': reports, 'report_types': MedicalReport.REPORT_TYPES,
        'filter_type': filter_type, 'filter_status': filter_status,
    })


@login_required
def report_detail(request, pk):
    report = get_object_or_404(MedicalReport, pk=pk, user=request.user)
    def parse_json_field(field):
        if field:
            try:
                return json.loads(field)
            except:
                return []
        return []
    raw_analysis = parse_json_field(report.raw_analysis) if isinstance(parse_json_field(report.raw_analysis), dict) else {}
    if report.raw_analysis:
        try:
            raw_analysis = json.loads(report.raw_analysis)
        except:
            raw_analysis = {}
    context = {
        'report': report,
        'raw_analysis': raw_analysis,
        'key_findings': parse_json_field(report.key_findings),
        'medications': parse_json_field(report.medications),
        'precautions': parse_json_field(report.precautions),
        'prevention': parse_json_field(report.prevention),
        'lifestyle_advice': parse_json_field(report.lifestyle_advice),
        'when_to_see_doctor': parse_json_field(report.when_to_see_doctor),
    }
    return render(request, 'report_detail.html', context)


@login_required
def delete_report(request, pk):
    report = get_object_or_404(MedicalReport, pk=pk, user=request.user)
    if request.method == 'POST':
        report.file.delete()
        report.delete()
        messages.success(request, 'Report deleted successfully.')
        return redirect('report_list')
    return render(request, 'confirm_delete.html', {'report': report})


@login_required
@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        report_id = data.get('report_id')
        conversation_history = data.get('history', [])
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        report_context = None
        report = None
        if report_id:
            try:
                report = MedicalReport.objects.get(pk=report_id, user=request.user)
                if report.raw_analysis:
                    report_context = json.loads(report.raw_analysis)
            except:
                pass
        context_str = "\n".join([f"{m['role']}: {m['content']}" for m in conversation_history[-4:]])
        response = chat_with_ai(message, context=context_str, report_context=report_context)
        ChatMessage.objects.create(user=request.user, report=report, message=message, response=response)
        return JsonResponse({'response': response})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'profile.html')


@login_required
def manual_entry(request):
    from .gemini_service import generate_findings, generate_summary, predict_risk
    if request.method == 'POST':
        title = request.POST.get('title', '').strip() or 'Manual Entry Report'
        patient_name = request.POST.get('patient_name', '').strip()
        patient_age = request.POST.get('patient_age', '')
        
        # Collect all entered values
        param_fields = ['hemoglobin','wbc','platelets','rbc','fasting_glucose',
                        'total_cholesterol','hdl','ldl','triglycerides',
                        'tsh','t3','t4','urine_glucose','urine_protein','urine_ph','creatinine']
        
        extracted_values = {}
        for field in param_fields:
            val = request.POST.get(field, '').strip()
            if val:
                try:
                    extracted_values[field] = float(val)
                except ValueError:
                    pass
        
        if not extracted_values:
            messages.error(request, 'Please enter at least one value to analyze.')
            return render(request, 'manual_entry.html')
        
        # Determine report type from which tab was active
        active_tab = request.POST.get('active_tab', 'blood')
        tab_to_type = {'blood': 'blood_test', 'lipid': 'lipid_profile', 'thyroid': 'thyroid', 'urine': 'urine_test'}
        report_type = tab_to_type.get(active_tab, 'blood_test')
        
        try:
            risk_level, _ = predict_risk(extracted_values)
        except Exception:
            risk_level = 'medium'
        
        findings = generate_findings(extracted_values)
        summary = generate_summary(extracted_values, risk_level, report_type)
        
        # Create a placeholder file for the report
        import tempfile, os
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        tmp.write(f"Manual Entry Report\n{title}\n".encode())
        tmp.close()
        
        from django.core.files import File
        report = MedicalReport(
            user=request.user, title=title, report_type=report_type,
            patient_name=patient_name,
            patient_age=int(patient_age) if patient_age.isdigit() else None,
            status='completed', risk_level=risk_level,
            analysis_summary=summary,
            key_findings=json.dumps(findings['key_findings']),
            medications=json.dumps(findings['medications']),
            precautions=json.dumps(findings['precautions']),
            prevention=json.dumps(findings['prevention']),
            lifestyle_advice=json.dumps(findings['lifestyle_advice']),
            when_to_see_doctor=json.dumps(findings['when_to_see_doctor']),
            raw_analysis=json.dumps({
                'summary': summary, 'risk_level': risk_level,
                'key_findings': findings['key_findings'],
                'dietary_restrictions': findings['dietary_restrictions'],
                'positive_notes': findings['positive_notes'],
                'disclaimer': 'ML analysis — not a substitute for professional medical advice.',
                'extracted_values': extracted_values,
            }),
        )
        with open(tmp.name, 'rb') as f:
            report.file.save(f'manual_{title[:20]}.txt', File(f))
        report.save()
        os.unlink(tmp.name)
        
        messages.success(request, 'ML Analysis complete!')
        return redirect('report_detail', pk=report.pk)
    
    return render(request, 'manual_entry.html')
