from django.core.exceptions import ValidationError
from django.utils.translation import gettext


class SimplePasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 3:
            raise ValidationError(
                gettext("The password you entered is too short. It must contain at least 3 characters."),
                code='password_too_short',
            )

    def get_help_text(self):
        return gettext("The password you entered is too short. It must contain at least 3 characters.")