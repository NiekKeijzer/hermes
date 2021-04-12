from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView


class IndexView(LoginRequiredMixin, RedirectView):
    pattern_name = "site-list"
