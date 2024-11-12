from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = _("You're not authenticated! Please, log in.")

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect('login')


class SelfCheckMixin:
    permission_check_message = _(
        "You do not have permission to modify another user."
    )

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'get_object') and self.get_object() != request.user:
            messages.error(request, self.permission_check_message)
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)
