from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView   
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext
from task_manager.forms import SignUpForm, UserUpdateForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         gettext('User is signed up successfully.'))
        return response


class UsersListView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all().order_by('id')


def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, gettext('You have logged in.'))
            return redirect('index')
        else:
            messages.error(request, gettext(
                'Please insert right username and password. Both fields may be case sensitive'))
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, gettext('You have logged out.'))
    return redirect('index')


def user_update(request, pk):
    if not request.user.is_authenticated:
        messages.error(
            request,
            gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
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
    return render(request, 'update.html', {'form': form})


def user_delete(request, pk):
    if not request.user.is_authenticated:
        messages.error(
            request,
            gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('/login/')
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        messages.error(
            request,
            gettext("You do not have permission to delete another user."))
        return redirect('/users/')
    if request.method == 'POST':
        user.delete()
        messages.info(request, gettext("User is deleted successfully!"))
        return redirect('users')
    return render(request, 'delete.html', {'user': user})
