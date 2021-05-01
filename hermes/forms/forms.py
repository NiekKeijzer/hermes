from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .models import Form, Site

User: AbstractBaseUser = get_user_model()


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "domain"]


class FormForm(forms.ModelForm):
    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["site"] = forms.ModelChoiceField(
            queryset=Site.objects.filter(user=user)
        )

    class Meta:
        model = Form
        fields = ["name", "site", "enabled"]
        help_texts = {
            "enabled": _("Submissions to a disabled form will not be processed")
        }
