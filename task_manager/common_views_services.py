from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.decorators import login_required
from dataclasses import dataclass


@login_required
def object_list(request, model, template_name, context_name):
    objects = model.objects.all()
    return render(request, template_name, {context_name: objects})


@dataclass
class CreateConfig:
    form_class: object
    template_name: str
    success_url: str
    success_message: str


@login_required
def object_create(request, config: CreateConfig):
    if request.method == 'POST':
        form = config.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, gettext(config.success_message))
            return redirect(config.success_url)
    else:
        form = config.form_class()
    return render(request, config.template_name, {'form': form})


@dataclass
class UpdateConfig:
    model: object
    form_class: object
    template_name: str
    success_url: str
    success_message: str


@login_required
def object_update(request, pk, config: UpdateConfig):
    obj = get_object_or_404(config.model, pk=pk)
    if request.method == 'POST':
        form = config.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, gettext(config.success_message))
            return redirect(config.success_url)
    else:
        form = config.form_class(instance=obj)
    return render(request, config.template_name, {'form': form})


@dataclass
class DeleteConfig:
    model: object
    template_name: str
    success_url: str
    success_message: str
    in_use_message: str
    related_field: str


@login_required
def object_delete(request, pk, config: DeleteConfig):
    obj = get_object_or_404(config.model, pk=pk)
    if getattr(obj, config.related_field).exists():
        messages.error(request, gettext(config.in_use_message))
        return redirect(config.success_url)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, gettext(config.success_message))
        return redirect(config.success_url)
    return render(
        request,
        config.template_name,
        {config.model.__name__.lower(): obj}
    )
