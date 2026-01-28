from django.urls import path ,include
from .views import create_lead , generate_email

urlpatterns = [
   
    path("leads/create/", create_lead),
    path("leads/<int:lead_id>/generate-email/", generate_email),
    path("dashboard/", include("dashboard.urls")),
]

