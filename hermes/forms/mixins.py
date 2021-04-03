from django.db import models
from django.views.generic.detail import SingleObjectMixin


class UserSiteMixin:
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()

        return qs.filter(user=self.request.user)


class UserFormMixin:
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()

        return qs.filter(site__user=self.request.user)
