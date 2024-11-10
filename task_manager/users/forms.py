from django import forms
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import CustomUser
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        )


class UserUpdateForm(SignUpForm):
    password1 = forms.CharField(
        required=True
    )

    password2 = forms.CharField(
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exclude(
                pk=self.instance.pk).exists():
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        return username
