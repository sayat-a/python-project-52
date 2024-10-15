from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView   
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext
from task_manager.forms import SignUpForm


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
