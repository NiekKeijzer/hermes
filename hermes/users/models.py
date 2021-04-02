from typing import Any, List

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    Group,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(
        self, *, email: str, password: str = None, **extra_fields: Any
    ) -> "CustomUser":
        if not email:
            raise ValueError(_("Email must be set"))

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user: CustomUser = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()

        return user

    def create_superuser(
        self, *, email: str, password: str = None, **extra_fields: Any
    ) -> "CustomUser":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields["is_staff"]:
            raise ValueError(_("Superuser must be staff"))

        if not extra_fields["is_superuser"]:
            raise ValueError(_("Superuser must be superuser"))

        if not password:
            raise ValueError(_("Superuser must have a password"))

        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.email
