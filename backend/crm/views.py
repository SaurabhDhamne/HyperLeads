import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Lead, EmailDraft , LeadSource

FLASK_AI_URL = "http://127.0.0.1:5001/score"
FLASK_EMAIL_URL = "http://127.0.0.1:5001/generate-email"


@csrf_exempt
def generate_email(request, lead_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    lead = Lead.objects.get(id=lead_id)

    ai_response = requests.post(
        FLASK_EMAIL_URL,
        json={
            "company_name": lead.company_name,
            "industry": lead.industry,
            "keywords": []
        }
    )

    if ai_response.status_code != 200:
        return JsonResponse(
            {
                "error": "AI service unavailable",
                "details": ai_response.text
            },
            status=503
        )

    # ✅ THIS MUST BE OUTSIDE THE IF
    data = ai_response.json()
    email_body = data.get("email")

    EmailDraft.objects.create(
        lead=lead,
        subject=f"Quick idea for {lead.company_name}",
        body=email_body
    )

    return JsonResponse(
        {
            "message": "Email generated successfully",
            "email": email_body
        }
    )

@csrf_exempt
def ingest_lead(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)

    # 1️⃣ Create or get source
    source_data = data.get("source", {})
    source, _ = LeadSource.objects.get_or_create(
        name=source_data.get("name", "Unknown Source"),
        defaults={
            "source_type": source_data.get("type", "MANUAL"),
            "platform": source_data.get("platform"),
            "campaign": source_data.get("campaign"),
        }
    )

    # 2️⃣ Create lead
    lead = Lead.objects.create(
        company_name=data["company_name"],
        email=data["email"],
        website=data.get("website"),
        industry=data.get("industry", "Unknown"),
        source=source
    )

    # 3️⃣ AI scoring
    ai_response = requests.post(
        FLASK_AI_URL,
        json={
            "industry": lead.industry,
            "website_text": lead.website or ""
        }
    )

    if ai_response.status_code == 200:
        lead.lead_score = ai_response.json()["lead_score"]
        lead.save()

    return JsonResponse({
        "message": "Lead ingested successfully",
        "lead_id": lead.id,
        "lead_score": lead.lead_score
    })


@csrf_exempt
def create_lead(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)

    lead = Lead.objects.create(
        company_name=data["company_name"],
        email=data["email"],
        website=data.get("website", ""),
        industry=data["industry"]
    )

    ai_response = requests.post(
        FLASK_AI_URL,
        json={
            "industry": lead.industry,
            "website_text": lead.website or ""
        }
    )

    ai_data = ai_response.json()
    lead.lead_score = ai_data["lead_score"]
    lead.save()

    return JsonResponse(
        {
            "message": "Lead created successfully",
            "lead_score": lead.lead_score
        }
    )
