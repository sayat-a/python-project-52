from django.shortcuts import render, redirect, get_object_or_404
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
            messages.success(request,
                             gettext("Status is successfully created"))
            return redirect('statuses_list')
    else:
        form = StatusForm()
    return render(request, 'statuses/status_form.html', {'form': form})


@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                gettext("Status is successfully updated"))
            return redirect('statuses_list')
    else:
        form = StatusForm(instance=status)
    return render(request, 'statuses/status_form.html', {'form': form})


@login_required
def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    # if status.task_set.exists():
    #    messages.error(
    #        request,
    #        gettext("Cannot delete status because it is in use"))
    #    return redirect('statuses_list')
    if request.method == 'POST':
        status.delete()
        messages.success(
            request,
            gettext("Status is successfully deleted"))
        return redirect('statuses_list')
    return render(request,
                  'statuses/status_delete.html',
                  {'status': status})
