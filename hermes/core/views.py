from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import info
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import RedirectView


class IndexView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        site = self.request.user.site_set.first()
        if site:
            return reverse("form-list", kwargs={"site_pk": site.pk})
        else:
            info(_("You don't have any sites yet, create one to get started"))

            return reverse("site-create")
