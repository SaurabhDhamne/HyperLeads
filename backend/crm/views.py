import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from .models import Lead, EmailDraft, LeadSource


FLASK_AI_URL = "http://127.0.0.1:5001/score"
FLASK_EMAIL_URL = "http://127.0.0.1:5001/generate-email"


# -----------------------------
# AI Lead Scoring Helper
# -----------------------------
def score_lead(lead):
    try:
        ai_response = requests.post(
            FLASK_AI_URL,
            json={
                "industry": lead.industry,
                "requirement": lead.requirement or ""
            },
            timeout=5
        )

        print("AI STATUS:", ai_response.status_code)
        print("AI RESPONSE:", ai_response.text)
        if ai_response.status_code == 200:
            data = ai_response.json()
            lead.lead_score = data.get("lead_score", 0)
            lead.save()

    except Exception as e:
        print("SCORING ERROR:", e)


# -----------------------------
# Add Lead (Dashboard Form)
# -----------------------------
def add_lead(request):
    if request.method == "POST":
        lead = Lead.objects.create(
            company_name=request.POST["company_name"],
            contact_name=request.POST.get("contact_name", ""),
            email=request.POST["email"],
            phone=request.POST.get("phone", ""),
            industry=request.POST.get("industry", ""),
            requirement=request.POST.get("requirement", ""),
        )

        score_lead(lead)
        return redirect("leads")

    return render(request, "dashboard/add_lead.html")


# -----------------------------
# Generate AI Email
# -----------------------------
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

    data = ai_response.json()
    email_body = data.get("email", "")

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


# -----------------------------
# Google Sheets / API Ingestion
# -----------------------------
@csrf_exempt
def ingest_lead(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    leads_data = payload if isinstance(payload, list) else [payload]
    created_leads = []

    for data in leads_data:
        source_name = data.get("source", "Google Sheets")

        source, _ = LeadSource.objects.get_or_create(
            name=source_name,
            defaults={"source_type": "SHEET"}
        )

        lead = Lead.objects.create(
            company_name=data.get("company_name", ""),
            contact_name=data.get("contact_name", ""),
            email=data.get("email"),
            phone=data.get("phone", ""),
            industry=data.get("industry", ""),
            requirement=data.get("requirement", ""),
            lead_source=source
        )

        score_lead(lead)
        created_leads.append(lead.id)

    return JsonResponse({
        "message": "Leads ingested successfully",
        "count": len(created_leads),
        "lead_ids": created_leads
    })


# -----------------------------
# API-based Lead Creation
# -----------------------------
@csrf_exempt
def create_lead(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)

    lead = Lead.objects.create(
        company_name=data["company_name"],
        email=data["email"],
        website=data.get("website", ""),
        industry=data["industry"],
        requirement=data.get("requirement", "")

    )

    score_lead(lead)

    return JsonResponse(
        {
            "message": "Lead created successfully",
            "lead_score": lead.lead_score
        }
    )
