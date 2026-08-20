from django.core.management.base import BaseCommand
from django.utils import timezone
from phishing.models import PhishingCampaign, PhishingResult
from phishing.utils import send_phishing_email


class Command(BaseCommand):
    help = 'Send phishing emails for running campaigns'

    def handle(self, *args, **options):
        campaigns = PhishingCampaign.objects.filter(status='running')
        
        if not campaigns.exists():
            self.stdout.write(self.style.WARNING('No running campaigns found.'))
            return
        
        for campaign in campaigns:
            self.stdout.write(f'Sending emails for: {campaign.name}')
            
            # Get employees in the campaign's departments
            employees = []
            for dept in campaign.departments.all():
                employees.extend(dept.employees.all())
            
            if not employees:
                self.stdout.write(self.style.WARNING(f'  - No employees in department for campaign: {campaign.name}'))
                continue
            
            sent_count = 0
            for employee in employees:
                # Check if already sent
                if PhishingResult.objects.filter(campaign=campaign, employee=employee).exists():
                    self.stdout.write(f'  - Skipping {employee.email} (already sent)')
                    continue
                
                # Send email
                success = send_phishing_email(employee, campaign, campaign.template)
                
                if success:
                    # Record the result
                    PhishingResult.objects.create(
                        campaign=campaign,
                        employee=employee,
                        status='sent',
                        opened_at=None,
                        clicked_at=None,
                        submitted_at=None,
                        reported_at=None
                    )
                    sent_count += 1
                    self.stdout.write(f'  - Sent to {employee.email}')
                else:
                    self.stdout.write(f'  - Failed to send to {employee.email}')
            
            self.stdout.write(self.style.SUCCESS(f'✅ Sent {sent_count} emails for {campaign.name}'))