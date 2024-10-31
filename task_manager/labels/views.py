from task_manager.labels.models import Label
from django.utils.translation import gettext
from task_manager.labels.forms import LabelForm
from task_manager.common_views_services import (
    object_list,
    object_create,
    object_update,
    object_delete
)


# Create your views here.
def labels_list(request):
    return object_list(
        request,
        Label,
        'labels/labels_list.html',
        'labels'
    )


def label_create(request):
    return object_create(
        request,
        LabelForm,
        'labels/label_form.html',
        'labels_list',
        gettext("Label is successfully created")
    )


def label_update(request, pk):
    return object_update(
        request,
        pk,
        Label,
        LabelForm,
        'labels/label_form.html',
        'labels_list',
        gettext("Label is successfully updated")
    )


def label_delete(request, pk):
    return object_delete(
        request,
        pk,
        Label,
        'labels/label_delete.html',
        'labels_list',
        gettext("Label is successfully deleted"),
        gettext("Cannot delete label because it is in use"),
        'task_set'
    )
