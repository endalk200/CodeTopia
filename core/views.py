# Built in modules

# Django related modules
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import (
    render,
)

from django.views.generic.base import View

from django.utils.translation import gettext, gettext_lazy as _

# Third party modules


__all__ = [
    "Homepage",
    "Elements"
]

class Homepage(View):
    """Homepage View"""
    template_name = "core/index.html"
    title = _("CodeTopia")
    extra_context = None

    def get_context_data(self, **kwargs):
        current_site = get_current_site(self.request)
        context = {
            'site': current_site,
            'site_name': current_site.name,
            'title': self.title,
            **(self.extra_context or {})
        }
        return context

    def get(self, *args, **kwargs):
        return render(
            request=self.request, 
            template_name=self.template_name, 
            context=self.get_context_data())

class Elements(View):
    """Homepage View"""
    template_name = "core/elements.html"
    title = _("CodeTopia | Elements")
    extra_context = None

    def get_context_data(self, **kwargs):
        current_site = get_current_site(self.request)
        context = {
            'site': current_site,
            'site_name': current_site.name,
            'title': self.title,
            **(self.extra_context or {})
        }
        return context

    def get(self, *args, **kwargs):
        return render(
            request=self.request, 
            template_name=self.template_name, 
            context=self.get_context_data())
