import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .symptom_data import SYMPTOMS, CONDITIONS, SPECIALISTS
from .ml_engine import analyze_symptoms, train_symptom_model, model_exists


def symptom_checker(request):
    if not model_exists():
        train_symptom_model()

    # Group symptoms by body part
    by_part = {}
    for key, sym in SYMPTOMS.items():
        part = sym['body_part']
        if part not in by_part:
            by_part[part] = []
        by_part[part].append({'key': key, **sym})

    return render(request, 'symptom_checker/checker.html', {
        'symptoms': SYMPTOMS,
        'symptoms_json': json.dumps({k: v for k, v in SYMPTOMS.items()}),
        'by_part': by_part,
        'specialists': SPECIALISTS,
    })


@require_POST
def analyze_api(request):
    try:
        data = json.loads(request.body)
        selected = data.get('symptoms', [])
        age = data.get('age', '')
        gender = data.get('gender', '')

        if not selected:
            return JsonResponse({'error': 'Please select at least one symptom.'}, status=400)

        if len(selected) > 20:
            return JsonResponse({'error': 'Please select fewer symptoms (max 20).'}, status=400)

        result = analyze_symptoms(selected)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
