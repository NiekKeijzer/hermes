from typing import Tuple

from django.utils.translation import gettext as _

from hermes.forms.models import Submission
from hermes.utils.email import EmailBody, render_email_body


def render_submission_body(*, submission: Submission) -> Tuple[str, EmailBody]:
    subject = _("New submission on %(form)s") % {"form": submission.form}
    body = render_email_body(
        "hooks/mail/submission.html",
        context={
            "subject": subject,
            "submission": submission,
        },
    )

    return subject, body
