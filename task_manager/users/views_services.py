from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth import login
from django.shortcuts import render, redirect
from task_manager.users.forms import UserUpdateForm


def is_authenticated_(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            gettext("You're not authenticated! Please, log in.")
        )
        return False
    return True


def has_permission(request, user):
    if request.user != user:
        messages.error(
            request,
            gettext("You do not have permission to modify another user.")
        )
        return False
    return True


def run_update_post_request(request, user):
    form = UserUpdateForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        login(request, user)
        messages.success(request, gettext("User is updated successfully!"))
        return redirect('/users/')
    return render(request, 'users/update.html', {'form': form})
