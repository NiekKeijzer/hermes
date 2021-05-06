from django.contrib.auth import get_user_model
from django.db import models

from .utils import generate_token

User = get_user_model()


class Site(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Form(models.Model):
    hash = models.CharField(max_length=32, db_index=True, default=generate_token)

    name = models.CharField(max_length=255, db_index=True)
    enabled = models.BooleanField(default=True)

    validate_referrer = models.BooleanField(default=True)
    redirect_url = models.URLField(blank=True, null=True)

    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


class Submission(models.Model):
    received_at = models.DateTimeField(auto_now=True)
    data = models.JSONField()

    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Submission on {self.form} at {self.received_at.isoformat()}"
