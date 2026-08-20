from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import PhishingResult


@csrf_exempt
def track_phishing_click(request, campaign_id, employee_id):
    """Track when an employee clicks the phishing link"""
    result = get_object_or_404(
        PhishingResult, 
        campaign_id=campaign_id, 
        employee_id=employee_id
    )
    
    # Update tracking information
    result.status = 'clicked'
    result.clicked_at = timezone.now()
    result.ip_address = request.META.get('REMOTE_ADDR')
    result.user_agent = request.META.get('HTTP_USER_AGENT', '')
    result.save()
    
    print(f"✅ Click tracked: {result.employee.email} - {result.campaign.name} - {result.clicked_at}")
    
    # Redirect to educational page (no login required)
    return HttpResponseRedirect('/phishing/education/')


def phishing_education(request):
    """Show educational content after clicking phishing link"""
    return render(request, 'phishing/education.html')