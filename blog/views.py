# Built in modules

# Django related modules
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import (
    render, 
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    resolve_url
)
from django.http import HttpResponseGone
from django.urls import (
    reverse,
    reverse_lazy
)

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

from django.utils.translation import gettext, gettext_lazy as _
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)

from django.views.decorators.cache import never_cache

from django.views.generic.base import View
from django.views.generic.edit import FormView

from django.contrib import messages

# Project modules
from .forms import BlogCreatioForm

from .models import Blog

# Third party modules
import markdown2


__all__ = [
    "BlogIndexView",
    "CreateBlog",
    "BlogDetail",
    "UpdateBlog"
]

class BlogIndexView(View):
    """Class for creating user with no priviledges"""

    template_name = "blog/index.html"

    title = _('CodeTopia | Blog')
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        """Return all context data by collecting it."""
        current_site = get_current_site(self.request)
        context = {
            "site": current_site,
            "site_name": current_site.name,
            "title": self.title
        }
        context.update(**(self.extra_context or {}))
        return context

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            "blogs": Blog.blogs.all()
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())


class CreateBlog(View):
    """class creating a blog from given fields"""
    template_name = "blog/create_blog.html"
    form_class = BlogCreatioForm

    title = _('CodeTopia | Create Blog')
    extra_context = None

    # Error messages for the view
    error_messages = {
    }
    # Success messages for the view
    success_messages = {
        "created_succesfully": _("Congradulation you have created  your blog succesfully.")
    }

    def get_form_class(self, *args, **kwargs):
        """Return the instance of the for class to be used."""
        return self.form_class(*args)

    def get_context_data(self, *args, **kwargs):
        """Return all context data by collecting it."""
        current_site = get_current_site(self.request)
        context = {
            "site": current_site,
            "site_name": current_site.name,
            "title": self.title
        }
        context.update(**(self.extra_context or {}))
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.extra_context = {
            "form": self.get_form_class()
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())

    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    def post(self, *args, **kwargs):
        form = self.get_form_class(self.request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = self.request.user
            blog.title = markdown2.markdown(text=form.cleaned_data.get("title"))
            blog.subject = markdown2.markdown(text=form.cleaned_data.get("subject"))
            blog.body = markdown2.markdown(text=form.cleaned_data.get("body"))
            blog.save()
            messages.success(
                request=self.request, 
                message=self.success_messages.get("created_succesfully")
            )

            return HttpResponseRedirect(reverse(viewname="blog:blog_homepage"))

        # If the form is invalid return the form with error messages
        self.extra_context = {
            **self.get_context_data(),
            "form": form
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())


class BlogDetail(View):
    """Class for updating user with no priviledges"""
    template_name = "blog/blog_detail.html"

    title = _('CodeTopia | Blog Detail')
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        """Return all context data by collecting it."""
        current_site = get_current_site(self.request)
        context = {
            "site": current_site,
            "site_name": current_site.name,
            "title": self.title
        }
        context.update(**(self.extra_context or {}))
        return context

    def get_blog_instance(self, *args, **kwargs):
        return Blog.objects.get(id=int(self.kwargs["id"]))

    def get(self, request, *args, **kwargs):

        self.extra_context = {
            "blog": self.get_blog_instance()
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())


class UpdateBlog(View, UserPassesTestMixin):
    """Class for updating user with no priviledges"""
    template_name = "blog/update_blog.html"
    form_class = BlogCreatioForm

    title = _('CodeTopia | Update Blog')
    extra_context = None

    # Error messages for the view
    error_messages = {
    }
    # Success messages for the view
    success_messages = {
        "updated_succesfully": _("Congradulation you have updated  your blog succesfully.")
    }

    def get_form_class(self, *args, **kwargs):
        """Return the instance of the for class to be used."""
        return self.form_class(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Return all context data by collecting it."""
        current_site = get_current_site(self.request)
        context = {
            "site": current_site,
            "site_name": current_site.name,
            "title": self.title
        }
        context.update(**(self.extra_context or {}))
        return context

    def get_blog_instance(self, *args, **kwargs):
        return Blog.objects.get(id=int(self.kwargs["id"]))

    def test_func(self):
        return self.request.user == self.get_blog_instance().author

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        self.extra_context = {
            "form": self.get_form_class(instance=self.get_blog_instance())
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        form = self.get_form_class(self.request.POST, instance=self.get_blog_instance())
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = self.request.user
            blog.title = markdown2.markdown(text=form.cleaned_data.get("title"))
            blog.subject = markdown2.markdown(text=form.cleaned_data.get("subject"))
            blog.body = markdown2.markdown(text=form.cleaned_data.get("body"))
            blog.save()
            messages.success(
                request=self.request, 
                message=self.success_messages.get("updated_succesfully")
            )

            return HttpResponseRedirect(reverse(viewname="blog:blog_homepage"))

        # If the form is invalid return the form with error messages
        self.extra_context = {
            **self.get_context_data(),
            "form": form
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())
