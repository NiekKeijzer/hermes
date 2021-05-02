from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .models import Form, Site

User: AbstractBaseUser = get_user_model()


class SiteForm(forms.ModelForm):
    url = forms.URLField()

    class Meta:
        model = Site
        fields = ["name", "url"]


class FormForm(forms.ModelForm):
    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["site"] = forms.ModelChoiceField(
            queryset=Site.objects.filter(user=user)
        )

    class Meta:
        model = Form
        fields = ["name", "site", "enabled", "validate_referrer", "redirect_url"]
        help_texts = {
            "enabled": _("Submissions to a disabled form will not be processed"),
            "validate_referrer": _(""),
            "redirect_url": _(
                "If none is specified, user will be redirected to where they came from"
            ),
        }
