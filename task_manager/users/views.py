from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from task_manager.users.models import CustomUser
from task_manager.users.forms import SignUpForm, UserUpdateForm
from task_manager.users.mixins import CustomLoginRequiredMixin, SelfCheckMixin
from task_manager.mixins import DeletionCheckMixin


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
    success_message = _('User is signed up successfully.')


class UsersListView(ListView):
    model = CustomUser
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    queryset = CustomUser.objects.all().order_by('id')


class UserUpdateView(
    CustomLoginRequiredMixin,
    SelfCheckMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _("User is updated successfully!")


class UserDeleteView(
    CustomLoginRequiredMixin,
    SelfCheckMixin,
    DeletionCheckMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = CustomUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    error_message = _("Cannot delete user because it is in use")
    success_message = _("User is deleted successfully!")

    def has_dependencies(self, user):
        return user.task_set.exists() or user.created_tasks.exists()
