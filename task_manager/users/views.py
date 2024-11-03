from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
    )
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext
from django.contrib.auth.models import User
from task_manager.users.forms import SignUpForm, UserUpdateForm
from django.db.models import ProtectedError


# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         gettext('User is signed up successfully.'))
        return response


class UsersListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all().order_by('id')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance = self.request.user
        return form

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                gettext("You're not authenticated! Please, log in."))
            return redirect('login')
        if self.get_object() != request.user:
            messages.error(request, gettext(
                "You do not have permission to modify another user."))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, gettext(
            "User is updated successfully!"))
        return response


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                gettext("You're not authenticated! Please, log in."))
            return redirect('login')
        if self.get_object() != request.user:
            messages.error(
                request,
                gettext("You do not have permission to modify another user."))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.info(
                self.request,
                gettext("User is deleted successfully!"))
            return response
        except ProtectedError:
            messages.error(
                self.request,
                gettext("Cannot delete user because it is in use"))
            return redirect(self.success_url)
