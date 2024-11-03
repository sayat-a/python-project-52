from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext
from django.urls import reverse_lazy


def index(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    next_page = 'index'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, gettext('You have logged in.'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, gettext(
            'Please insert the correct username and password. '
            'Both fields may be case sensitive.'))
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, gettext('You have logged out.'))
        return super().dispatch(request, *args, **kwargs)
