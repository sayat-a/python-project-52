from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.models import User
from task_manager.users.forms import SignUpForm, UserUpdateForm
from django.contrib.auth import login
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


def user_update(request, pk):
    if not request.user.is_authenticated:
        messages.error(
            request,
            gettext("You're not authenticated! Please, log in."))
        return redirect('/login/')
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        messages.error(
            request,
            gettext("You do not have permission to modify another user."))
        return redirect('/users/')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            login(request, user)
            messages.success(request, gettext("User is updated successfully!"))
            return redirect('/users/')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/update.html', {'form': form})


def user_delete(request, pk):
    if not request.user.is_authenticated:
        messages.error(
            request,
            gettext("You're not authenticated! Please, log in."))
        return redirect('/login/')
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        messages.error(
            request,
            gettext("You do not have permission to delete another user."))
        return redirect('/users/')
    if request.method == 'POST':
        try:
            user.delete()
            messages.info(request, gettext("User is deleted successfully!"))
        except ProtectedError:
            messages.error(
                request,
                gettext("Cannot delete user because it is in use"))
            return redirect('users')
        return redirect('users')

    return render(request, 'users/delete.html', {'user': user})
