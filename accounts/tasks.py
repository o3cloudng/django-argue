from time import sleep
from django.core.mail import send_mail


def send_feedback_email_task(email_address, message):
    """Sends an email when the feedback form has been submitted."""
    sleep(20)  # Simulate expensive operation(s) that freeze Django
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        "olumideo@synercomgroup.net",
        [email_address],
        fail_silently=False,
    )
