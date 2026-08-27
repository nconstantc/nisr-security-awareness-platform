from rest_framework import generics, permissions
from .models import PhishingCampaign, PhishingTemplate, PhishingResult, PhishingReport
from .serializers import (
    PhishingCampaignSerializer,
    PhishingTemplateSerializer,
    PhishingResultSerializer,
    PhishingReportSerializer
)


class PhishingTemplateListView(generics.ListCreateAPIView):
    """List and create phishing templates"""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingTemplate.objects.all().order_by("-created_at")
    serializer_class = PhishingTemplateSerializer


class PhishingTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete a phishing template"""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingTemplate.objects.all()
    serializer_class = PhishingTemplateSerializer


class PhishingCampaignListView(generics.ListCreateAPIView):
    """List and create phishing campaigns"""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingCampaign.objects.all().order_by('-created_at')
    serializer_class = PhishingCampaignSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PhishingCampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete a phishing campaign"""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingCampaign.objects.all()
    serializer_class = PhishingCampaignSerializer


class PhishingResultListView(generics.ListAPIView):
    """List phishing results"""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingResult.objects.all().order_by('-id')
    serializer_class = PhishingResultSerializer


class PhishingReportListView(generics.ListAPIView):
    """List employee phishing reports for Console administrators."""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingReport.objects.select_related('employee', 'reviewed_by').all().order_by('-reported_at')
    serializer_class = PhishingReportSerializer


class PhishingReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View and review an employee phishing report."""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingReport.objects.select_related('employee', 'reviewed_by').all()
    serializer_class = PhishingReportSerializer

    def perform_update(self, serializer):
        report = serializer.save()
        review_fields = {'status', 'notes', 'is_phishing'}
        if review_fields.intersection(self.request.data.keys()):
            from django.utils import timezone
            report.reviewed_by = self.request.user
            report.reviewed_at = timezone.now()
            report.save(update_fields=['reviewed_by', 'reviewed_at'])


# ========== SEND PHISHING EMAILS ENDPOINT ==========

from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.core.management import call_command
from io import StringIO


@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def send_phishing_campaigns(request):
    """Trigger the send_phishing management command"""
    try:
        out = StringIO()
        call_command('send_phishing', stdout=out)
        output = out.getvalue()
        
        return JsonResponse({
            'success': True,
            'message': 'Phishing emails sent successfully',
            'output': output
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)