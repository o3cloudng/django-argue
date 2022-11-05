from django.core.mail import EmailMessage
from django.conf import settings
# from accounts.tasks import send_feedback_email_task


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()

        # send_feedback_email_task.delay(email.send())
