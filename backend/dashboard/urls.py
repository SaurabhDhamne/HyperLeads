from django.urls import path
from .views import leads_view, email_drafts_view

urlpatterns = [
    path("leads/", leads_view, name="leads"),
    path("emails/", email_drafts_view, name="emails"),
]
