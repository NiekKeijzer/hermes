from functools import wraps
from typing import Callable

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest

from .models import Form


def validate_referrer(view_func: Callable) -> Callable:
    def wrapper_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        _hash = kwargs.get("hash")
        if _hash is None:
            raise ValueError("Form hash is needed to validate the referrer")

        form = Form.objects.filter(hash__exact=_hash, enabled=True).get()
        if form.validate_referrer:
            referrer = request.META.get("HTTP_REFERER")
            if not isinstance(referrer, str) or not referrer.startswith(form.site.url):
                return HttpResponseBadRequest()

        return view_func(request, *args, **kwargs)

    return wraps(view_func)(wrapper_view)
