from django.urls import path ,include
from .views import create_lead , generate_email , ingest_lead , add_lead

urlpatterns = [
   
    path("leads/create/", create_lead),
    path("leads/<int:lead_id>/generate-email/", generate_email),
    path("dashboard/", include("dashboard.urls")),
    path("leads/ingest/", ingest_lead),
    path("dashboard/leads/add/",add_lead, name="add_lead"),


]

