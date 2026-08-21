from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Badge, EmployeeBadge


def download_badge_certificate(request, badge_id):
    """Generate a certificate for an earned badge"""
    
    employee_badge = get_object_or_404(
        EmployeeBadge,
        id=badge_id,
        employee=request.user
    )
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{employee_badge.badge.name}_certificate.txt"'
    response.write('=' * 60 + '\n')
    response.write('           CERTIFICATE OF ACHIEVEMENT\n')
    response.write('=' * 60 + '\n\n')
    response.write(f'This certifies that\n\n')
    response.write(f'    {employee_badge.employee.full_name}\n\n')
    response.write(f'has successfully earned the\n\n')
    response.write(f'    "{employee_badge.badge.name}" Badge\n\n')
    response.write(f'Awarded on: {employee_badge.awarded_at.strftime("%B %d, %Y")}\n\n')
    response.write('-' * 60 + '\n')
    response.write('National Institute of Statistics of Rwanda\n')
    response.write('Information Security Training Program\n')
    
    return response