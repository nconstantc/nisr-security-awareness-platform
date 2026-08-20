from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_phishing_email(employee, campaign, template):
    """Send phishing simulation email to employee"""
    subject = template.subject
    html_message = template.body
    plain_message = strip_tags(html_message)
    from_email = 'nconstantine521@gmail.com'

    print(f"=== SENDING EMAIL ===")
    print(f"To: {employee.email}")
    print(f"From: {from_email}")
    print(f"Subject: {subject}")
    print(f"====================")

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[employee.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"✅ Email sent to {employee.email}")
        return True
    except Exception as e:
        print(f"❌ Error sending to {employee.email}: {e}")
        return False