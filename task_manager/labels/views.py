from django.shortcuts import render, redirect, get_object_or_404
from task_manager.labels.models import Label
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext
from task_manager.labels.forms import LabelForm


# Create your views here.
@login_required
def labels_list(request):
    labels = Label.objects.all()
    return render(request,
                  'labels/labels_list.html',
                  {'labels': labels})
    

@login_required
def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             gettext("Label is successfully created"))
            return redirect('labels_list')
    else:
        form = LabelForm()
    return render(request, 'labels/label_form.html', {'form': form})


@login_required
def label_update(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                gettext("Label is successfully updated"))
            return redirect('labels_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'labels/label_form.html', {'form': form})


@login_required
def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if label.task_set.exists():
        messages.error(
            request,
            gettext("Cannot delete label because it is in use"))
        return redirect('labels_list')
    if request.method == 'POST':
        label.delete()
        messages.success(
            request,
            gettext("Label is successfully deleted"))
        return redirect('labels_list')
    return render(request,
                  'labels/label_delete.html',
                  {'label': label})
