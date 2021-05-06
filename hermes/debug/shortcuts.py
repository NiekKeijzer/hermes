import importlib
from typing import Generator

from django.apps import apps
from django.urls import include, path
from django.urls.resolvers import URLResolver


def discover_debug_urls() -> Generator[None, URLResolver, None]:
    for app in apps.get_app_configs():
        if "hermes" not in app.name:
            continue

        url_module = f"{app.module.__name__}.debug.urls"
        try:
            debug_urls = importlib.import_module(url_module)
        except ImportError:
            continue

        yield path(f"{app.verbose_name.lower()}/", include(debug_urls))
