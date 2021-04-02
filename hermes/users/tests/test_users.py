import pytest
from django.contrib.auth.models import Group

from hermes.users.models import CustomUser


def test_create_user() -> None:
    user = CustomUser.objects.create_user(
        email="testy@example.com", password="password"
    )

    assert user.email == "testy@example.com"
    assert str(user) == "testy@example.com"
    assert user.is_active
    assert not user.is_superuser
    assert not user.is_staff
    assert user.check_password("password")


def test_user_in_users_group(users_group: Group) -> None:
    user = CustomUser.objects.create_user(
        email="testy@example.com", password="password"
    )

    assert users_group in user.groups.all()


def test_create_user_no_email() -> None:
    with pytest.raises(ValueError):
        CustomUser.objects.create_user(email="")


def test_create_user_unusable_password() -> None:
    user = CustomUser.objects.create_user(email="testy@example.com")

    assert not user.has_usable_password()


def test_create_superuser() -> None:
    su = CustomUser.objects.create_superuser(
        email="su@example.com", password="password"
    )

    assert su.email == "su@example.com"
    assert su.is_active
    assert su.is_superuser
    assert su.check_password("password")


def test_create_superuser_not_staff() -> None:
    with pytest.raises(ValueError):
        CustomUser.objects.create_superuser(
            email="su@example.com", password="password", is_staff=False
        )


def test_create_superuser_not_superuser() -> None:
    with pytest.raises(ValueError):
        CustomUser.objects.create_superuser(
            email="su@example.com", password="password", is_superuser=False
        )


def test_create_superuser_unusable_password() -> None:
    with pytest.raises(ValueError):
        CustomUser.objects.create_superuser(email="su@example.com")
