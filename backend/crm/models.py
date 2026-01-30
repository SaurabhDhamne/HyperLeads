from django.db import models

# lead Source model
class LeadSource(models.Model):
    SOURCE_TYPES = [
        ("ADS", "Ads"),
        ("SCRAPER", "Scraper"),
        ("SHEET", "Google Sheet"),
        ("MANUAL", "Manual"),
        ("WEBHOOK", "Webhook"),
    ]

    name = models.CharField(max_length=255)   # e.g. "Google Ads – SaaS"
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    platform = models.CharField(max_length=100, blank=True, null=True)
    campaign = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.source_type})"



class Lead(models.Model):

    lead_source = models.ForeignKey(
        LeadSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
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
    source = models.ForeignKey(
        LeadSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.lead_score})"


# Email draft model
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

