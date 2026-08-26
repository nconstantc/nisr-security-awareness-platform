from rest_framework import serializers
from .models import PhishingCampaign, PhishingTemplate, PhishingResult, PhishingReport


class PhishingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhishingTemplate
        fields = ['id', 'name', 'subject', 'body', 'sender_name', 'sender_email', 'landing_page_url', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PhishingCampaignSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    template_subject = serializers.CharField(source='template.subject', read_only=True)
    
    class Meta:
        model = PhishingCampaign
        fields = ['id', 'name', 'template', 'template_name', 'template_subject', 
                  'course', 'departments', 'status', 'start_date', 'end_date', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']


class PhishingResultSerializer(serializers.ModelSerializer):
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    
    class Meta:
        model = PhishingResult
        fields = ['id', 'campaign', 'campaign_name', 'employee', 'employee_email',
                  'status', 'opened_at', 'clicked_at', 'submitted_at', 'reported_at']

class PhishingReportSerializer(serializers.ModelSerializer):
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    employee_name = serializers.SerializerMethodField()
    reviewed_by_email = serializers.CharField(source='reviewed_by.email', read_only=True)

    class Meta:
        model = PhishingReport
        fields = [
            'id', 'employee', 'employee_name', 'employee_email',
            'sender_email', 'subject', 'body_preview', 'reason',
            'status', 'reported_at', 'reviewed_at', 'reviewed_by',
            'reviewed_by_email', 'notes', 'is_phishing'
        ]
        read_only_fields = [
            'employee', 'employee_name', 'employee_email', 'reported_at',
            'reviewed_at', 'reviewed_by', 'reviewed_by_email'
        ]

    def get_employee_name(self, obj):
        return obj.employee.get_full_name() or obj.employee.email
