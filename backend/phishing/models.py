from django.db import models
from django.conf import settings
from courses.models import Course
from accounts.models import Department


class PhishingTemplate(models.Model):
    """Phishing email template"""
    name = models.CharField("Template Name", max_length=255)
    subject = models.CharField("Email Subject", max_length=255)
    body = models.TextField("Email Body")
    sender_name = models.CharField("Sender Name", max_length=255)
    sender_email = models.CharField("Sender Email", max_length=255)
    landing_page_url = models.URLField("Landing Page URL", blank=True, null=True)
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class PhishingCampaign(models.Model):
    """Phishing simulation campaign"""
    DRAFT = 'draft'
    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (SCHEDULED, 'Scheduled'),
        (RUNNING, 'Running'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    name = models.CharField("Campaign Name", max_length=255)
    template = models.ForeignKey(
        PhishingTemplate, 
        on_delete=models.PROTECT, 
        related_name="campaigns"
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.PROTECT, 
        related_name="phishing_campaigns", 
        null=True, 
        blank=True
    )
    departments = models.ManyToManyField(
        Department, 
        blank=True, 
        related_name="phishing_campaigns"
    )
    start_date = models.DateTimeField("Start Date")
    end_date = models.DateTimeField("End Date", null=True, blank=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="phishing_campaigns"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class PhishingResult(models.Model):
    """Individual phishing simulation result"""
    SENT = 'sent'
    OPENED = 'opened'
    CLICKED = 'clicked'
    SUBMITTED = 'submitted'
    REPORTED = 'reported'
    FAILED = 'failed'
    
    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (OPENED, 'Opened'),
        (CLICKED, 'Clicked'),
        (SUBMITTED, 'Submitted'),
        (REPORTED, 'Reported'),
        (FAILED, 'Failed'),
    ]
    
    campaign = models.ForeignKey(
        PhishingCampaign, 
        on_delete=models.CASCADE, 
        related_name="results"
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="phishing_results"
    )
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default=SENT)
    opened_at = models.DateTimeField("Opened At", null=True, blank=True)
    clicked_at = models.DateTimeField("Clicked At", null=True, blank=True)
    submitted_at = models.DateTimeField("Submitted At", null=True, blank=True)
    reported_at = models.DateTimeField("Reported At", null=True, blank=True)
    ip_address = models.GenericIPAddressField("IP Address", null=True, blank=True)
    user_agent = models.TextField("User Agent", blank=True)

    def __str__(self):
        return f"{self.employee.email} - {self.campaign.name} - {self.status}"

    class Meta:
        unique_together = ['campaign', 'employee']


class PhishingReport(models.Model):
    """Employee report of suspicious email"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('investigating', 'Under Investigation'),
        ('confirmed_phishing', 'Confirmed Phishing'),
        ('false_positive', 'False Positive'),
        ('resolved', 'Resolved'),
    ]
    
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="phishing_reports"
    )
    sender_email = models.CharField("Sender Email", max_length=255)
    subject = models.CharField("Email Subject", max_length=255)
    body_preview = models.TextField("Email Body Preview", blank=True)
    reason = models.TextField("Why do you think this is suspicious?")
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_reports"
    )
    notes = models.TextField("Admin Notes", blank=True)
    is_phishing = models.BooleanField("Was this actually phishing?", null=True, blank=True)

    def __str__(self):
        return f"{self.employee.email} - {self.subject} - {self.status}"

    class Meta:
        ordering = ['-reported_at']