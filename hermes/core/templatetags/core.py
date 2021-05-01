from typing import Any

from django import template
from django.http import HttpRequest
from django.shortcuts import reverse
from django.template.context import RequestContext

register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(
    context: RequestContext, view_name: str, *args: Any, **kwargs: Any
) -> str:
    request: HttpRequest = context["request"]

    return request.build_absolute_uri(reverse(view_name, args=args, kwargs=kwargs))


@register.filter(name="dict_key")
def dict_key(data: dict, key: str, default: Any = None) -> Any:
    return data.get(key, default)
