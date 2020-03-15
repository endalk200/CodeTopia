# Built in modules

# Django related modules
from django import forms

from django.utils.translation import gettext, gettext_lazy as _

# Project modules
from .models import Blog

# Third party modules

__all__ = [ 
    "BlogCreatioForm"
]

class BlogCreatioForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """

    error_messages = {
    }

    help_texts = {
    }

    class Meta:
        model = Blog
        exclude = ["author", "published"]
        labels = {
            'author': Blog._meta.get_field("author").verbose_name
        }
        help_texts = {
            'title': _('Keep it short and brief ')
        }
        error_messages = {
            'profile_picture': {
                'file_too_large': _("The file is too large."),
            },
        }
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'subject': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'published': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'body': forms.Textarea(attrs={
                'cols': 80, 'rows': 20, 'class': 'form-control'
            })
        }
