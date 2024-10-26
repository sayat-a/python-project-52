from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
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
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=gettext(
                    'Insert right username. It may contain only letters, '
                    'numbers, and @/./+/-/_ characters.'),
            )
        ],
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
        self._validate_password_strength(password1)
        self._check_passwords_match(password1, password2)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def _validate_password_strength(self, password):
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as e:
                self.add_error('password2', e)

    def _check_passwords_match(self, password1, password2):
        if password1 and password2 and password1 != password2:
            self.add_error('password2', gettext("Passwords are not equal."))
