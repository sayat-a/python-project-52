from django.shortcuts import render, redirect, get_object_or_404
from task_manager.tags.models import Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext
from task_manager.tags.forms import TagForm


# Create your views here.
@login_required
def tags_list(request):
    tags = Tag.objects.all()
    return render(request,
                  'tags/tags_list.html',
                  {'tags': tags})


@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             gettext("Tag is successfully created"))
            return redirect('tags_list')
    else:
        form = TagForm()
    return render(request, 'tags/tag_form.html', {'form': form})


@login_required
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                gettext("Tag is successfully updated"))
            return redirect('tags_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tags/tag_form.html', {'form': form})


@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    # if tag.task_set.exists():
    #    messages.error(
    #        request,
    #        gettext("Cannot delete tag because it is in use"))
    #    return redirect('tags_list')
    if request.method == 'POST':
        tag.delete()
        messages.success(
            request,
            gettext("Tag is successfully deleted"))
        return redirect('tags_list')
    return render(request,
                  'tags/tag_delete.html',
                  {'tag': tag})
