from typing import List, Optional

from django import forms
from django.apps import AppConfig, apps


class HookConfig(AppConfig):
    def get_settings_form(self, **kwargs) -> forms.Form:
        """
        :param kwargs:
        :return:
        """
        raise NotImplemented("`get_settings_form_class` must be overridden")

    @classmethod
    def get_hooks(cls) -> List["HookConfig"]:
        return [app for app in apps.get_app_configs() if isinstance(app, cls)]

    @classmethod
    def get_hook(cls, name: Optional[str]) -> "HookConfig":
        for app in cls.get_hooks():
            if name == app.name:
                return app
        else:
            raise LookupError(f"No hook found by {name}")
