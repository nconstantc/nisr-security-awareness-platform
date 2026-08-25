from rest_framework import serializers
from .models import PhishingCampaign, PhishingTemplate, PhishingResult


class PhishingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhishingTemplate
        fields = ['id', 'name', 'subject', 'sender_name', 'sender_email', 'is_active']


class PhishingCampaignSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    template_subject = serializers.CharField(source='template.subject', read_only=True)
    
    class Meta:
        model = PhishingCampaign
        fields = ['id', 'name', 'template', 'template_name', 'template_subject', 
                  'status', 'start_date', 'end_date', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']


class PhishingResultSerializer(serializers.ModelSerializer):
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    
    class Meta:
        model = PhishingResult
        fields = ['id', 'campaign', 'campaign_name', 'employee', 'employee_email',
                  'status', 'opened_at', 'clicked_at', 'submitted_at', 'reported_at']