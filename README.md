# 🏥 MediReport — AI Medical Report Analyzer

A full-stack Django web app where users upload medical reports (PDF/images) and Google Gemini AI analyzes them — providing key findings, medication info, precautions, prevention tips, and a floating MediBot chatbot on every page.

---

## 🗂️ Project Structure

```
medireport/
├── medireport/          # Django project config
│   ├── settings.py
│   └── urls.py
├── reports/             # Main app
│   ├── models.py        # MedicalReport, ChatMessage models
│   ├── views.py         # All page views + chat API
│   ├── urls.py          # URL routing
│   ├── admin.py         # Django admin config
│   └── gemini_service.py # Gemini AI integration
├── templates/           # HTML templates
│   ├── base.html        # Base layout + MediBot chatbot
│   ├── home.html        # Landing page
│   ├── dashboard.html   # User dashboard
│   ├── upload.html      # Report upload page
│   ├── report_detail.html # Full AI analysis view
│   ├── report_list.html # All reports list
│   ├── login.html
│   ├── register.html
│   └── profile.html
├── static/              # CSS, JS, images
├── media/               # Uploaded report files
├── .env.example         # Environment variable template
└── manage.py
```

---

## ⚡ Quick Setup

### 1. Install dependencies
```bash
pip install django pillow python-dotenv
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

Get your free Gemini API key at: https://aistudio.google.com/app/apikey

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create admin user (optional)
```bash
python manage.py createsuperuser
```

### 5. Start the server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🔑 Environment Variables (.env)

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Note:** Without a Gemini API key, the app runs in demo mode with sample analysis output.

---

## ✨ Features

### 📋 Universal Report Analysis
- Supports **any** medical report type: blood tests, MRI, X-Ray, CT scan, ECG, lipid profile, thyroid, liver/kidney function, urine analysis, and more
- Accepts **PDF** and **image** files (JPG, PNG, WEBP) up to 10MB
- Powered by **Google Gemini 1.5 Flash** (vision + text)

### 🔍 Analysis Output
- **Summary** — plain-language overview of findings
- **Key Findings** — each parameter with value, normal range, and status (Normal / High / Low / Abnormal)
- **Risk Level** — Low / Medium / High / Critical with color coding
- **Medications** — possible medications (informational only)
- **Precautions** — what to be careful about
- **Prevention** — how to prevent worsening
- **Lifestyle Advice** — diet, exercise, sleep tips
- **When to See a Doctor** — red flag symptoms
- **Dietary Restrictions** — foods to avoid
- **Positive Notes** — what looks healthy

### 🤖 MediBot Chatbot
- Floating chat button on **every page** (bottom-right)
- Context-aware: knows which report you're viewing
- Quick-reply chips for common questions
- Chat history maintained per session
- All conversations saved to database

### 👤 User Management
- Register / Login / Logout
- Profile page
- Each user sees only their own reports

### 📊 Dashboard
- Stats: total reports, analyzed, pending, high-risk count
- Recent reports table with status and risk badges
- Quick upload shortcut

### 🔧 Django Admin
- Full admin panel at `/admin/`
- Manage reports, users, chat messages

---

## 🗄️ Database Models

### MedicalReport
| Field | Type | Description |
|-------|------|-------------|
| user | FK(User) | Owner |
| title | CharField | Report name |
| report_type | CharField | blood_test, mri, xray, etc. |
| file | FileField | Uploaded PDF/image |
| status | CharField | pending / analyzing / completed / failed |
| risk_level | CharField | low / medium / high / critical |
| analysis_summary | TextField | AI summary text |
| key_findings | TextField | JSON list of findings |
| medications | TextField | JSON list |
| precautions | TextField | JSON list |
| prevention | TextField | JSON list |
| lifestyle_advice | TextField | JSON list |
| when_to_see_doctor | TextField | JSON list |
| raw_analysis | TextField | Full Gemini JSON response |

### ChatMessage
| Field | Type | Description |
|-------|------|-------------|
| user | FK(User) | Who sent the message |
| report | FK(MedicalReport) | Optional linked report |
| message | TextField | User's question |
| response | TextField | AI's answer |

---

## 🌐 URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | home | Landing page |
| `/register/` | register_view | Sign up |
| `/login/` | login_view | Sign in |
| `/logout/` | logout_view | Sign out |
| `/dashboard/` | dashboard | User dashboard |
| `/upload/` | upload_report | Upload & analyze |
| `/reports/` | report_list | All reports |
| `/reports/<id>/` | report_detail | Full analysis view |
| `/reports/<id>/delete/` | delete_report | Delete report |
| `/api/chat/` | chat_api | MediBot JSON API |
| `/profile/` | profile | Edit profile |
| `/admin/` | Django admin | Admin panel |

---

## 🚀 Production Deployment

For production, also install:
```bash
pip install gunicorn whitenoise psycopg2-binary
```

Change in settings.py:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medireport_db',
        # ... PostgreSQL credentials
    }
}
```

Run with Gunicorn:
```bash
gunicorn medireport.wsgi:application --bind 0.0.0.0:8000
```

---

## ⚠️ Disclaimer

MediReport is for **informational purposes only**. It does not provide medical diagnoses or replace professional medical advice. Always consult a qualified healthcare provider for medical decisions.
