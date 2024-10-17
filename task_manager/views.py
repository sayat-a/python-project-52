from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext


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
            messages.error(request,
                           gettext(
                               'Please insert right username and password. '
                               'Both fields may be case sensitive'))
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, gettext('You have logged out.'))
    return redirect('index')
