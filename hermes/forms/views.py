from typing import Any, Type

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import info
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from hermes.generic.mixins import AssignUserMixin, UserFormKwargsMixin

from .forms import FormForm, SiteForm
from .mixins import SiteFormMixin, UserFormMixin, UserSiteMixin
from .models import Form, Site


class SiteListView(LoginRequiredMixin, UserSiteMixin, ListView):
    model = Site


class SiteCreateView(LoginRequiredMixin, UserSiteMixin, AssignUserMixin, CreateView):
    model = Site
    form_class = SiteForm
    success_url = reverse_lazy("form-create")

    def form_valid(self, form: forms.ModelForm) -> HttpResponseRedirect:
        info(self.request, _("Site %(site)s created") % {"site": form.instance})

        return super().form_valid(form)


class SiteUpdateView(LoginRequiredMixin, UserSiteMixin, UpdateView):
    model = Site
    form_class = SiteForm


class SiteDeleteView(LoginRequiredMixin, UserSiteMixin, DeleteView):
    model = Site
    template_name = "generic/confirm_delete.html"
    success_url = reverse_lazy("site-list")


class FormListView(LoginRequiredMixin, UserFormMixin, SiteFormMixin, ListView):
    model = Form


class FormCreateView(
    LoginRequiredMixin, UserFormKwargsMixin, SiteFormMixin, CreateView
):
    model = Form
    form_class = FormForm

    success_url = reverse_lazy("form-list")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not Site.objects.filter(user=request.user).count():
            info(
                request,
                _(
                    "You don't have any sites yet, create have to create one first before you can create a form"
                ),
            )

            return redirect("site-create")

        return super(FormCreateView, self).get(request, *args, **kwargs)

    def get_form(self, form_class: Type[FormForm] = None) -> FormForm:
        form = super().get_form(form_class=form_class)
        if site_pk := self.kwargs.get("site_pk"):
            site = Site.objects.get(pk=site_pk)
            form.initial["site"] = site

        return form


class FormUpdateView(
    LoginRequiredMixin, UserFormMixin, UserFormKwargsMixin, SiteFormMixin, UpdateView
):
    model = Form
    form_class = FormForm


class FormDeleteView(LoginRequiredMixin, UserFormMixin, DeleteView):
    model = Form
    template_name = "generic/confirm_delete.html"
    success_url = reverse_lazy("form-list")
