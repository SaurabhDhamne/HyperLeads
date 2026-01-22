from django.contrib import admin

# Register your models here.

from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("company_name", "email", "industry", "lead_score", "status")
    list_filter = ("status", "industry")
    search_fields = ("company_name", "email")
