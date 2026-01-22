from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Lead

FLASK_AI_URL = "http://127.0.0.1:5001/score"

@csrf_exempt
def create_lead(request):
    if request.method == "POST":
        data = json.loads(request.body)

        lead = Lead.objects.create(
            company_name=data["company_name"],
            email=data["email"],
            website=data.get("website", ""),
            industry=data["industry"]
        )

        # Send data to Flask AI service
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

        return JsonResponse({
            "message": "Lead created successfully",
            "lead_score": lead.lead_score
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
