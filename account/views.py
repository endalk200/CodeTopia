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

from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)

from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

# Decorator for protecting clickjack attack
from django.views.decorators.clickjacking import xframe_options_exempt
# Browsers that support X-Frame-Options
    # Internet Explorer 8+
    # Edge
    # Firefox 3.6.9+
    # Opera 10.5+
    # Safari 4+
    # Chrome 4.1+

from django.utils.translation import gettext, gettext_lazy as _
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)

from django.views.decorators.cache import never_cache

from django.views.generic.base import View
from django.views.generic.edit import FormView

from django.contrib import messages

# Project modules
from .forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
    PasswordChangeForm,
    ProfileUpdateForm,
    UserUpdateForm
)

# Third party modules


__all__ = [
    "CustomLoginView",
    "CustomLogoutView",
    "CustomPasswordResetView",
    "CustomPasswordResetDoneView",
    "CustomPasswordResetConfirmView",
    "CustomPasswordResetCompleteView",
    "CreateUserView",
    "PrivateUserDashboard",
    "UserPasswordChangeView",
    "ProfileUpdate"
]

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class CreateUserView(View):
    """Class for creating user with no priviledges"""

    template_name = "account/create_account.html"

    form_class = UserCreationForm
    title = _('CodeTopia | Create Account')
    extra_context = None

    # Error messages for the view
    error_messages = {
        "already_have_account": _("You already have an account and can not create another account.")
    }
    # Success messages for the view
    success_messages = {
        "account_created": _("Congradulation %s you have created  an account succesfully.")
    }

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

    def get_form_class(self, *args, **kwargs):
        """Return the instance of the for class to be used."""
        return self.form_class(*args)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(request=self.request, message=self.error_messages.get("already_have_account"))
            return HttpResponseRedirect(reverse("core:homepage"))

        self.extra_context = {
            "form": self.get_form_class()
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    def post(self, *args, **kwargs):
        form = self.get_form_class(self.request.POST)
        if form.is_valid():
            user_cache = form.save()
            messages.success(
                request=self.request, 
                message=self.success_messages.get("account_created") % user_cache.username 
            )

            return HttpResponseRedirect(reverse(viewname="account:user_login"))

        # If the form is invalid return the form with error messages
        self.extra_context = {
            **self.get_context_data(),
            "form": form
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())


class ProfileUpdate(View):
    """Class for creating user with no priviledges"""

    template_name = "account/dashboard/profile_edit.html"

    profile_form_class = ProfileUpdateForm
    user_form_class = UserUpdateForm

    title = _('CodeTopia | Update Profile')
    extra_context = None

    # Error messages for the view
    error_messages = {
        "already_have_account": _("You already have an account and can not create another account.")
    }
    # Success messages for the view
    success_messages = {
        "profile_updated": _("Congradulation %s you have updated your profile succesfully.")
    }

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

    def get_profile_form_class(self, *args, **kwargs):
        """Return the instance of the for class to be used."""
        return self.profile_form_class(*args)

    def get_user_form_class(self, *args, **kwargs):
        """Return the instance of the for class to be used."""
        return self.user_form_class(*args)

    def get(self, request, *args, **kwargs):

        self.extra_context = {
            "user_form": self.user_form_class(instance=request.user),
            "profile_form": self.profile_form_class(instance=request.user.profile)
        }
        return render(request=request, template_name=self.template_name, context=self.get_context_data())

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        user_form = self.user_form_class(instance=request.user, data=request.POST),
        profile_form = self.profile_form_class(
            instance=request.user.profile, 
            data=request.POST, 
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_cache = user_form.save()
            profile_form.save()
            messages.success(
                request=self.request, 
                message=self.success_messages.get("profile_updated") % user_cache.username 
            )

            return HttpResponseRedirect(reverse(viewname="account:user_dashboard"))

        # If the form is invalid return the form with error messages
        self.extra_context = {
            **self.get_context_data(),
            "user_form": user_form,
            "profile_form": profile_form
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "account/login.html"

    title = _("CodeTopia | Login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            # add extra hidden field with the redirect URL after login
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

    def get_redirect_url(self):
        """Return URL to redirect the logged in user if the URL is safe."""

        redirect_to = self.request.POST.get(
            # get redirect url from the hidden next field
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def form_valid(self, form):
        """If the user cridentials rae valid log in the user using login() method."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return redirect URL from redirect_field or return from settings.LOGIN_REDIRECT_URL."""

        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)


class CustomLogoutView(LogoutView):
    """Class for loging authenticated out"""
    extra_context = None
    next_page = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            'site': current_site,
            'site_name': current_site.name,
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'account/pwd_reset/password_reset_email.html'
    subject_template_name = 'account/pwd_reset/password_reset_subject.txt'
    # extra_email_context
    html_email_template_name = 'account/pwd_reset/password_reset_html_template.html'

    success_url = reverse_lazy('account:user_password_reset_done')
    title = _('CodeTopia | Request Password Reset')
    form_class = PasswordResetForm
    template_name = "account/pwd_reset/password_reset.html"
    extra_context = {
        "expiration_date": timezone.now()
    }

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/pwd_reset/password_reset_done.html"
    title = _('CodeTopia | Password Reset Sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy("account:user_password_reset_complete")

    title = _('CodeTopia | Enter New Password')
    template_name = "account/pwd_reset/password_reset_confirm.html"
    extra_context = {
        # add extra context to be passed
    }

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/pwd_reset/password_reset_complete.html"
    title = _('CodeTopia | Password Reset Complete')

    extra_context = None

    def get_context_data(self, **kwargs):
        # the super method is calling PasswordContextMixin from PasswordResetCompleteView
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context


class UserPasswordChangeView(PasswordContextMixin, FormView):
    """
    View for changing user password using validated old password.
    Interface for UserDashboard
    """
    form_class = PasswordChangeForm
    success_url = None
    template_name = "account/dashboard/change_password.html"
    title = _("CodeTopia | Chnage Password")

    success_messages = {
        "succesfull": _("You have successfully changed your password.")
    }

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url is not None:
            url = self.success_url.format(**self.object.__dict__)
        url = reverse(viewname="account:user_dashboard", kwargs={"username": self.request.user.username})
        return url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()

        # Log out the user from other sessions and update the current session with
        # new password hash
        update_session_auth_hash(self.request, form.user)

        # send password changed message
        messages.success(
            request=self.request, 
            message=self.success_messages.get("succesfull") 
        )

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class PrivateUserDashboard(View, UserPassesTestMixin):
    """
    UserDashboard where only the user can access
    """
    template_name = "account/dashboard/index.html"
    extra_context = None

    def is_owner(self, user, request, *args, **kwargs):
        return request.user.username == self.kwargs.get("username")

    def get_test_func(self, request, *args, **kwargs):
        return self.is_owner

    def get_context_data(self, **kwargs):
        context = {
            "title": _("CodeTopia | %s"% self.kwargs.get("username"))
        }
        return context

    @xframe_options_exempt
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        context["passed_user"] = request.user

        return render(request=request, template_name=self.template_name, context=context)
