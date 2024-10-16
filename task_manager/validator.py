from django.core.exceptions import ValidationError
from django.utils.translation import gettext


class SimplePasswordValidator:
    def __init__(self):
        print("SimplePasswordValidator initialized")

    def validate(self, password, user=None):
        print(f"Validating password: {password}")  # Добавлен вывод пароля
        if len(password) < 3:
            print("Password too short!")  # Добавлен вывод ошибки
            raise ValidationError(
                gettext("The password you entered is too short. It must contain at least 3 characters."),
                code='password_too_short',
            )

    def get_help_text(self):
        return gettext("The password you entered is too short. It must contain at least 3 characters.")
