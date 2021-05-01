"""
Submissions should be on a 'clean' url so we namespace them. Therefore it is up
 to the caller to determine what the final URL will look like.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("<str:hash>", views.FormSubmissionView.as_view(), name="form-submission")
]
