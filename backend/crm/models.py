from django.db import models


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


# 🔽 ADD THIS MODEL (THIS WAS MISSING)
class EmailDraft(models.Model):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="email_drafts"
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email draft for {self.lead.company_name}"
