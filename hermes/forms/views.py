from typing import Any, Optional, Type

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import info
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_q.tasks import async_task

from hermes.generic.mixins import AssignUserMixin, UserFormKwargsMixin

from .decorators import validate_referrer
from .forms import FormForm, SiteForm
from .mixins import SiteFormMixin, UserFormMixin, UserSiteMixin
from .models import Form, Site, Submission
from .utils import sanitize_and_flatten


class SiteListView(LoginRequiredMixin, UserSiteMixin, ListView):
    model = Site


class SiteCreateView(LoginRequiredMixin, UserSiteMixin, AssignUserMixin, CreateView):
    model = Site
    form_class = SiteForm
    success_url = reverse_lazy("form-create")

    def form_valid(self, form: forms.ModelForm) -> HttpResponseRedirect:
        info(self.request, _("Site %(site)s created") % {"site": form.instance})

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("form-list", kwargs={"site_pk": self.object.pk})


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
    template_name = "forms/form_create.html"

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
        form.initial["site"] = self.get_site()

        return form

    def get_success_url(self) -> str:
        return reverse(
            "form-update",
            kwargs={"pk": self.object.pk, "site_pk": self.kwargs.get("site_pk")},
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["site"] = self.get_site()

        return ctx

    def get_site(self) -> Optional[Site]:
        if site_pk := self.kwargs.get("site_pk"):
            site = Site.objects.get(pk=site_pk)
        else:
            site = None

        return site


class FormUpdateView(
    LoginRequiredMixin, UserFormMixin, UserFormKwargsMixin, SiteFormMixin, UpdateView
):
    model = Form
    form_class = FormForm

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)

        form: Form = self.get_object()
        paginator = Paginator(form.submission_set.order_by("-received_at"), 10)

        try:
            page = paginator.page(self.request.GET.get("page"))
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        ctx.update(
            {
                "submission_list": page,
                "columns": set().union(
                    *(submission.data.keys() for submission in page)
                ),
            }
        )

        return ctx


class FormDeleteView(LoginRequiredMixin, UserFormMixin, DeleteView):
    model = Form
    template_name = "generic/confirm_delete.html"

    def get_success_url(self) -> str:
        return reverse("form-list", kwargs={"site_pk": self.kwargs.get("site_pk")})


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(validate_referrer, name="dispatch")
class FormSubmissionView(RedirectView):
    def get(
        self, request: HttpRequest, hash: str = None, *args, **kwargs
    ) -> HttpResponseRedirect:
        form = get_object_or_404(Form, hash__exact=hash, enabled=True)

        data = dict(request.POST or request.GET)
        submission = Submission.objects.create(
            form=form, data=sanitize_and_flatten(data)
        )

        async_task("hermes.forms.tasks.dispatch_submission_received", submission)

        return HttpResponseRedirect(self.get_success_url(form))

    def get_success_url(self, form: Form) -> str:
        return form.redirect_url or self.request.META.get("HTTP_REFERER", form.site.url)
