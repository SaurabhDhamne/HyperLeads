from django.contrib import admin
from .models import Lead, EmailDraft , LeadSource


@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "source_type", "platform", "campaign", "created_at")
    list_filter = ("source_type", "platform")
    search_fields = ("name", "campaign")

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("company_name", "email", "industry", "lead_score", "status")
    list_filter = ("status", "industry")
    search_fields = ("company_name", "email")


@admin.register(EmailDraft)
class EmailDraftAdmin(admin.ModelAdmin):
    list_display = ("lead", "subject", "created_at")
    search_fields = ("subject", "body")
    list_filter = ("created_at",)

