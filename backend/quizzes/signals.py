from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from badges.models import Badge, EmployeeBadge
from .models import QuizAttempt

User = get_user_model()


@receiver(post_save, sender=QuizAttempt)
def award_badge_on_quiz_pass(sender, instance, created, **kwargs):
    """Automatically award badge when a user passes a quiz"""
    
    # Only award if the quiz was passed
    if not instance.passed:
        return
    
    # Get the course from the wave assignment
    wave_assignment = instance.wave_assignment
    if not wave_assignment:
        return
    
    wave = wave_assignment.wave
    course = wave.course
    
    # Find badges associated with this course
    badges = Badge.objects.filter(course=course, is_active=True)
    
    if not badges.exists():
        return
    
    # Award each badge to the employee
    employee = wave_assignment.employee
    
    for badge in badges:
        employee_badge, created = EmployeeBadge.objects.get_or_create(
            badge=badge,
            employee=employee
        )
        
        if created:
            print(f'✅ Badge "{badge.name}" awarded to {employee.email} for completing {course.title}')
        else:
            print(f'⚠️ Badge "{badge.name}" already awarded to {employee.email}')