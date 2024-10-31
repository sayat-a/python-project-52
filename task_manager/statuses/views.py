from task_manager.statuses.models import Status
from django.utils.translation import gettext
from task_manager.statuses.forms import StatusForm
from task_manager.common_views_services import (
    object_list,
    object_create,
    object_update,
    object_delete
)


# Create your views here.
def statuses_list(request):
    return object_list(
        request,
        Status,
        'statuses/statuses_list.html',
        'statuses'
    )


def status_create(request):
    return object_create(
        request,
        StatusForm,
        'statuses/status_form.html',
        'statuses_list',
        gettext("Status is successfully created")
    )


def status_update(request, pk):
    return object_update(
        request,
        pk,
        Status,
        StatusForm,
        'statuses/status_form.html',
        'statuses_list',
        gettext("Status is successfully updated")
    )


def status_delete(request, pk):
    return object_delete(
        request,
        pk,
        Status,
        'statuses/status_delete.html',
        'statuses_list',
        gettext("Status is successfully deleted"),
        gettext("Cannot delete status because it is in use"),
        'task_set'
    )
