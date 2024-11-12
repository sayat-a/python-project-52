from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = 'index'
    redirect_authenticated_user = True
    success_message = _('You have logged in.')

    def form_invalid(self, form):
        messages.error(self.request, _(
            'Please insert the correct username and password. '
            'Both fields may be case sensitive.'))
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You have logged out.'))
        return super().dispatch(request, *args, **kwargs)
