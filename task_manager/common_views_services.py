from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.decorators import login_required


@login_required
def object_list(request, model, template_name, context_name):
    objects = model.objects.all()
    return render(request, template_name, {context_name: objects})


@login_required
def object_create(
    request,
    form_class,
    template_name,
    success_url,
    success_message
):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, gettext(success_message))
            return redirect(success_url)
    else:
        form = form_class()
    return render(request, template_name, {'form': form})


@login_required
def object_update(
    request,
    pk,
    model,
    form_class,
    template_name,
    success_url,
    success_message
):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, gettext(success_message))
            return redirect(success_url)
    else:
        form = form_class(instance=obj)
    return render(request, template_name, {'form': form})


@login_required
def object_delete(
    request,
    pk,
    model,
    template_name,
    success_url,
    success_message,
    in_use_message,
    related_field
):
    obj = get_object_or_404(model, pk=pk)
    if getattr(obj, related_field).exists():
        messages.error(request, gettext(in_use_message))
        return redirect(success_url)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, gettext(success_message))
        return redirect(success_url)
    return render(request, template_name, {model.__name__.lower(): obj})
