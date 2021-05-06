from django.urls import path

from . import views

urlpatterns = [path("submission/", views.debug_submission_email)]
