from django.db import models

# Create your models here.


class Lead(models.Model):
    STATUS_CHOICES = [
        ("NEW", "New"),
        ("CONTACTED", "Contacted"),
        ("CONVERTED", "Converted"),
    ]

    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100)

    lead_score = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NEW"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.lead_score})"
