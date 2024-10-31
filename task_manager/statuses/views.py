from task_manager.statuses.models import Status
from django.utils.translation import gettext
from task_manager.statuses.forms import StatusForm
from task_manager.common_views_services import (
    object_list,
    object_create,
    object_update,
    object_delete,
    DeleteConfig,
    UpdateConfig,
    CreateConfig
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
    config = CreateConfig(
        form_class=StatusForm,
        template_name='statuses/status_form.html',
        success_url='statuses_list',
        success_message=gettext("Status is successfully created")
    )
    return object_create(request, config)


def status_update(request, pk):
    config = UpdateConfig(
        model=Status,
        form_class=StatusForm,
        template_name='statuses/status_form.html',
        success_url='statuses_list',
        success_message=gettext("Status is successfully updated")
    )
    return object_update(request, pk, config)


def status_delete(request, pk):
    config = DeleteConfig(
        model=Status,
        template_name='statuses/status_delete.html',
        success_url='statuses_list',
        success_message=gettext("Status is successfully deleted"),
        in_use_message=gettext("Cannot delete status because it is in use"),
        related_field='task_set'
    )
    return object_delete(request, pk, config)
