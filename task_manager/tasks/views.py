from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm


# Create your views here.
@login_required
def tasks_list(request):
    tasks = Task.objects.all()
    status_id = request.GET.get('status')
    executor_id = request.GET.get('executor')
    label_id = request.GET.get('label')
    self_tasks = request.GET.get('self_tasks')

    if status_id:
        tasks = tasks.filter(status_id=status_id)

    if executor_id:
        tasks = tasks.filter(executor_id=executor_id)

    if label_id:
        tasks = tasks.filter(labels__id=label_id)

    if self_tasks:
        tasks = tasks.filter(executor=request.user)

    statuses = Status.objects.all()
    executors = User.objects.all()
    labels = Label.objects.all()

    context = {
        'tasks': tasks,
        'statuses': statuses,
        'executors': executors,
        'labels': labels
    }

    return render(request, 'tasks/tasks_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            messages.success(request, gettext("Task is successfully created"))
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, gettext("Task is successfully updated"))
            return redirect('tasks_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.creator:
        messages.error(
            request,
            gettext("Task can be deleted only by it's creator"))
        return redirect('tasks_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, gettext("Task is successfully deleted"))
        return redirect('tasks_list')
    return render(request, 'tasks/task_delete.html', {'task': task})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})
