from django.shortcuts import redirect
from django.contrib import messages


class DeletionCheckMixin:

    def has_dependencies(self, obj):
        return False

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.has_dependencies(obj):
            messages.error(request, getattr(self, 'error_message'))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
