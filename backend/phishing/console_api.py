from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PhishingCampaign, PhishingTemplate, PhishingResult
from .serializers import (
    PhishingCampaignSerializer,
    PhishingTemplateSerializer,
    PhishingResultSerializer
)


class PhishingTemplateListView(generics.ListAPIView):
    """List all phishing templates"""
    permission_classes = [permissions.IsAdminUser]
    queryset = PhishingTemplate.objects.filter(is_active=True)
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


# ========== SEND PHISHING EMAILS ENDPOINT ==========

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from io import StringIO


@csrf_exempt
def send_phishing_campaigns(request):
    """Trigger the send_phishing management command"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
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