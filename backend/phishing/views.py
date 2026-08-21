from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PhishingResult, PhishingCampaign, PhishingReport





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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phishing_risk_employees(request):
    """Get employees who clicked phishing links"""
    user = request.user
    
    # Only staff can access this
    if not user.is_staff:
        return Response({'error': 'Permission denied'}, status=403)
    
    # Get employees who clicked phishing links
    clickers = PhishingResult.objects.filter(
        status__in=['clicked', 'submitted']
    ).values(
        'employee__id',
        'employee__email',
        'employee__full_name',
        'employee__department__name'
    ).annotate(
        click_count=Count('id')
    ).order_by('-click_count')
    
    # Get detailed results
    results = PhishingResult.objects.filter(
        status__in=['clicked', 'submitted']
    ).select_related('employee', 'campaign')
    
    data = []
    for r in results:
        data.append({
            'id': r.id,
            'employee_id': r.employee.id,
            'employee_name': r.employee.full_name,
            'employee_email': r.employee.email,
            'department': r.employee.department.name if r.employee.department else None,
            'campaign': r.campaign.name,
            'status': r.status,
            'clicked_at': r.clicked_at,
            'ip_address': r.ip_address,
        })
    
    return Response({
        'clickers': clickers,
        'results': data,
        'total_clickers': len(data)
    })
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phishing_risk_employees(request):
    """Get employees who clicked phishing links"""
    user = request.user
    
    # Only staff can access this
    if not user.is_staff:
        return Response({'error': 'Permission denied'}, status=403)
    
    # Get employees who clicked phishing links
    clickers = PhishingResult.objects.filter(
        status__in=['clicked', 'submitted']
    ).values(
        'employee__id',
        'employee__email',
        'employee__full_name',
        'employee__department__name'
    ).annotate(
        click_count=Count('id')
    ).order_by('-click_count')
    
    # Get detailed results
    results = PhishingResult.objects.filter(
        status__in=['clicked', 'submitted']
    ).select_related('employee', 'campaign')
    
    data = []
    for r in results:
        data.append({
            'id': r.id,
            'employee_id': r.employee.id,
            'employee_name': r.employee.full_name,
            'employee_email': r.employee.email,
            'department': r.employee.department.name if r.employee.department else None,
            'campaign': r.campaign.name,
            'status': r.status,
            'clicked_at': r.clicked_at,
            'ip_address': r.ip_address,
        })
    
    return Response({
        'clickers': clickers,
        'results': data,
        'total_clickers': len(data)
    })

@login_required
def report_phishing(request):
    """Employee reports a suspicious email"""
    if request.method == 'POST':
        sender_email = request.POST.get('sender_email', '')
        subject = request.POST.get('subject', '')
        body_preview = request.POST.get('body_preview', '')
        reason = request.POST.get('reason', '')
        
        report = PhishingReport.objects.create(
            employee=request.user,
            sender_email=sender_email,
            subject=subject,
            body_preview=body_preview,
            reason=reason,
        )
        
        messages.success(request, '✅ Thank you! Your report has been submitted for review.')
        return redirect('phishing-report-success')
    
    return render(request, 'phishing/report.html')


@login_required
def report_success(request):
    """Show success page after reporting"""
    return render(request, 'phishing/report_success.html')