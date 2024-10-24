from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


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
        widget=forms.PasswordInput(attrs={
            'placeholder': gettext('Confirm Password')})
    )

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2')


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label=gettext("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': gettext("Password"),
            'class': 'form-control'}),
        required=True
    )

    password2 = forms.CharField(
        label=gettext("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': gettext("Confirm Password"),
            'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1:
            try:
                validate_password(password1, self.instance)
            except ValidationError as e:
                self.add_error('password2', e)

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2',
                               gettext("Passwords are not equal."))

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
