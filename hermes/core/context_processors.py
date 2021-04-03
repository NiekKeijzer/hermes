from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


def current_site(request: HttpRequest) -> dict:
    return {"CURRENT_SITE": get_current_site(request)}
