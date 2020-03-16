# Built in modules
import unicodedata

# Django related modules
from django import forms

from django.template import loader

from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)

from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

from django.core.mail import EmailMultiAlternatives

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _

# Project modules
from .models import Profile

# Third party modules


UserModel = get_user_model()

__all__ = [ 
    "AuthenticationForm",
    "UserCreationForm",
    "PasswordChangeForm",
    "UserUpdateForm",
    "ProfileUpdateForm"
]

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        """Return HTML form attribute set for UserName field from CharField"""
        return {
            **super().widget_attrs(widget),
            "autofocus": True,
            "class": "form-control",
            "placeholder": "Enter Username",
            "aria-describedby": "emailHelp"
            # add extra HTML attributes for UsernameField
        }

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'email_exists': _('the email has already exists.'),
        'unsuported_email': _('invalid email: either your email host is invalid or is unsuported')
    }

    help_texts = {
        'email_help_text': _('Enter valid email host like: Gmail, Yahoo.'),
        'password2_help_text': _('Enter the same password as before, for verification.')
    }

    widget_attributes = {
        # add common HTML attributes
    }

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter email",
            **widget_attributes
        }),
        help_text=help_texts.get("email_help_text")
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter password",
            **widget_attributes
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter password again for confirmation",
            **widget_attributes
        }),
        strip=False,
        help_text=help_texts.get("password2_help_text"),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # check if there is username field in fields from User model
        if self._meta.model.USERNAME_FIELD in self.fields:
            # add widget attribute to the USERNAME_FIELD
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_username(self):
        return self.cleaned_data.get("username")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email.endswith("@gmail.com") or email.endswith("@yahoo.com"):
            try:
                users = User.objects.get(email=self.cleaned_data.get("email"))
            except User.DoesNotExist:
                return email
            except User.MultipleObjectsReturned:
                pass
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        else:
            raise forms.ValidationError(
                self.error_messages['unsuported_email'],
                code='unsuported_email',
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages.get("password_mismatch"),
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """

    error_messages = {
    }

    help_texts = {
    }

    class Meta:
        model = Profile
        exclude = ["user"]
        labels = {
            'profile_picture': Profile._meta.get_field("profile_picture").verbose_name
        }
        help_texts = {
            'profile_picture': _('Must be less than 5MB. Otherwise will '
                                'be compressed and loose some pixels'),
        }
        error_messages = {
            'profile_picture': {
                'file_too_large': _("The file is too large."),
            },
        }
        widgets = {
            'phone_number_1': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone_number_2': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'education_background': forms.Select(attrs={
                'class': 'form-control'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'github_url': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'personal_url': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'facebook_account': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'twitter_account': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'linkedin_account': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'short_bio': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 80, 'rows': 5
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 80, 'rows': 10
            }),
            'availability': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

    def _post_clean(self):
        super()._post_clean()


class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name = 'auth/widgets/read_only_password_hash.html'
    read_only = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': gettext("No password set.")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': gettext(key), 'value': value_})
        context['summary'] = summary
        return context


class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        field_classes = {'username': UsernameField}

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            })
        }


class AuthenticationForm(forms.Form):
    """AuthenticationForm: Form authenticating user using username and password"""

    # Create Fields for The User Authentication
    username = UsernameField(label=_("Username"), strip=False )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "form-control",
            "placeholder": "Enter Password"
            # add extra HTML attributes for password
        }),
    )

    # Error Messages: error message to be rendered incase of form.is_valid() returns False
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
            The 'request' parameter is set for custom auth use by subclasses.
            The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

        # Set maximum_length property to the UerNameField
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length

        # set HTML attribute maxlength to max_length retrieved either from the UserModel or Default
        self.fields['username'].widget.attrs['maxlength'] = username_max_length

        # if the username field has no label
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        """ return clean data by authenticating the cridentials"""

        if self.cleaned_data.get('username') is not None and self.cleaned_data.get('password'):
            # authenticate will return user instance is the user exists and authenticated
            self.user_cache = authenticate(
                request=self.request,
                username=self.cleaned_data.get('username'), 
                password=self.cleaned_data.get('password'))
            if self.user_cache is None:
                # if there is no user with the cridentials get_invalid_login_error()
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        # if authenticate returns a user
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method raises raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            # if the user is not active the raise inactive error_message
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autofocus": True
        })
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
        self, domain_override=None,
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name='registration/password_reset_email.html',
        use_https=False, token_generator=default_token_generator,
        from_email=None, request=None, html_email_template_name=None,
        extra_email_context=None
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'
        }),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        # return user instance if the commit=False is set
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        # inherite error_message from SetPassword Form and add extra error_messages
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True
        }),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
            Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password