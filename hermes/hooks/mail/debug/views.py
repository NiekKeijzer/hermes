from django.http import HttpRequest, HttpResponse

from hermes.forms.models import Form, Site, Submission
from hermes.hooks.mail.email import render_submission_body


def debug_submission_email(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    (site, _) = Site.objects.get_or_create(
        name="test site", url="https://example.com", user=request.user
    )
    (form, _) = Form.objects.get_or_create(name="test form", site=site)
    submission = form.submission_set.first()
    if submission is None:
        submission = Submission.objects.create(
            form=form, data={"name": "Testy", "message": "This is a test message"}
        )

    (_, body) = render_submission_body(submission=submission)

    return HttpResponse(body.html)
