from django.db import models

from hermes.forms.models import Form


class FormMailSettings(models.Model):
    email_address = models.EmailField()
    enabled = models.BooleanField(default=False)

    form = models.OneToOneField(Form, on_delete=models.CASCADE)

    def __str__(self):
        return self.email_address
