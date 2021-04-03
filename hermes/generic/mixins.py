from django import forms
from django.core.exceptions import FieldDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin


class AssignUserMixin(FormMixin):
    def form_valid(self, form: forms.ModelForm) -> HttpResponseRedirect:
        instance = form.save(commit=False)
        try:
            instance._meta.get_field("user")
            instance.user = self.request.user
        except FieldDoesNotExist:
            pass

        instance.save()

        return HttpResponseRedirect(self.get_success_url())


class UserFormKwargsMixin(FormMixin):
    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs.setdefault("user", self.request.user)

        return kwargs
