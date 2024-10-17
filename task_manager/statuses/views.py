from django.shortcuts import render, redirect
from task_manager.statuses.models import Status
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext
from task_manager.statuses.forms import StatusForm


# Create your views here.
@login_required
def statuses_list(request):
    statuses = Status.objects.all()
    return render(request,
                  'statuses/statuses_list.html',
                  {'statuses': statuses})


@login_required
def status_create(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, gettext("Status successfully created"))
            return redirect('statuses_list')
    else:
        form = StatusForm()
    return render(request, 'statuses/status_form.html', {'form': form})
