from django import forms

from .models import FormMailSettings


class FormMailSettingsForm(forms.ModelForm):
    class Meta:
        model = FormMailSettings
        fields = ("email_address", "enabled")

    def __init__(self, **kwargs):
        self.form_object = kwargs.pop("form")

        kwargs.setdefault("instance", self.form_object.formmailsettings)
        super().__init__(**kwargs)

    def save(self, commit=True):
        self.instance.form = self.form_object

        return super().save(commit)
