from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=255,
        label=gettext("First Name"),
        widget=forms.TextInput(attrs={'placeholder': gettext('First Name')})
    )
    last_name = forms.CharField(
        max_length=255,
        label=gettext("Last Name"),
        widget=forms.TextInput(attrs={'placeholder': gettext('Last Name')})
    )
    username = forms.CharField(
        max_length=150,
        label=gettext("Username"),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': gettext('Username')})
    )

    password1 = forms.CharField(
        label=gettext("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': gettext('Password')})
    )

    password2 = forms.CharField(
        label=gettext("Confirm Password"),
        widget=forms.PasswordInput(attrs={'placeholder': gettext('Confirm Password')})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
