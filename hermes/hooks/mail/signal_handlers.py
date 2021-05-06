from django.core.mail import send_mail

from hermes.forms.models import Submission
from hermes.forms.signals import submission_received
from hermes.utils.email import render_email_body

from .email import render_submission_body
from .models import FormMailSettings


def send_submission_to_email(submission: Submission, **kwargs) -> None:
    try:
        settings = FormMailSettings.objects.filter(form=submission.form).first()
    except FormMailSettings.DoesNotExist:
        return

    (subject, body) = render_submission_body(submission=submission)

    send_mail(
        subject=subject,
        message=body.plain,
        from_email=None,
        html_message=body.html,
        recipient_list=[settings.email_address],
    )


def connect_signals() -> None:
    submission_received.connect(send_submission_to_email)
