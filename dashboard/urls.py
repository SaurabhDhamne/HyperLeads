from django.urls import path
from .views import leads_view, email_drafts_view , lead_detail_view

urlpatterns = [
    path("leads/", leads_view, name="leads"),
    path("emails/", email_drafts_view, name="emails"),
    path("leads/<int:lead_id>/", lead_detail_view, name="lead_detail"),
]
