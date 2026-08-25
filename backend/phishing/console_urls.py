from django.urls import path
from . import console_api

urlpatterns = [
    path('templates/', console_api.PhishingTemplateListView.as_view(), name='console-phishing-templates'),
    path('templates/<int:pk>/', console_api.PhishingTemplateDetailView.as_view(), name='console-phishing-template-detail'),
    path('campaigns/', console_api.PhishingCampaignListView.as_view(), name='console-phishing-campaigns'),
    path('campaigns/<int:pk>/', console_api.PhishingCampaignDetailView.as_view(), name='console-phishing-campaign-detail'),
    path('results/', console_api.PhishingResultListView.as_view(), name='console-phishing-results'),
    path('send/', console_api.send_phishing_campaigns, name='console-phishing-send'),
]