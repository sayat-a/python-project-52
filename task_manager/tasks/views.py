from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filter import TaskFilter


# Create your views here.
class TaskListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_filter(self, filterset_class):
        filterset = super().get_filterset(filterset_class)
        filterset.request = self.request
        return filterset


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
