from django.db import models

from .models import Site


class UserSiteMixin:
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()

        return qs.filter(user=self.request.user)


class UserFormMixin:
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()

        site_pk = self.kwargs.get("site_pk")
        if site_pk is not None:
            qs = qs.filter(site_id=site_pk)

        return qs.filter(site__user=self.request.user)


class SiteFormMixin:
    """ Adds the related site object to the temlate context """

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        if site_pk := self.kwargs.get("site_pk"):
            ctx["site"] = Site.objects.get(pk=site_pk)

        return ctx
