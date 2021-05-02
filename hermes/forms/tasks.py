from hermes.forms.models import Submission

from .signals import submission_received


def dispatch_submission_received(submission: Submission) -> None:
    submission_received.send_robust(dispatch_submission_received, submission=submission)
