import typing

from hermes.hooks import HookConfig

if typing.TYPE_CHECKING:
    from .forms import FormMailSettingsForm


class MailConfig(HookConfig):
    name = "hermes.hooks.mail"

    def ready(self):
        from .signal_handlers import connect_signals

        connect_signals()

    def get_settings_form(self, **kwargs) -> "FormMailSettingsForm":
        from .forms import FormMailSettingsForm

        return FormMailSettingsForm(**kwargs)
