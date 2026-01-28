

# Create your views here.
from django.shortcuts import render
from crm.models import Lead, EmailDraft

def leads_view(request):
    leads = Lead.objects.all().order_by("-created_at")
    return render(request, "dashboard/leads.html", {"leads": leads})







def email_drafts_view(request):
    emails = EmailDraft.objects.all().order_by("-created_at")
    return render(request, "dashboard/emails.html", {"emails": emails})
