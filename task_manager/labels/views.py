from task_manager.labels.models import Label
from django.utils.translation import gettext
from task_manager.labels.forms import LabelForm
from task_manager.common_views_services import (
    object_list,
    object_create,
    object_update,
    object_delete,
    DeleteConfig,
    CreateConfig,
    UpdateConfig
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
    config = CreateConfig(
        form_class=LabelForm,
        template_name='labels/label_form.html',
        success_url='labels_list',
        success_message=gettext("Label is successfully created")
    )
    return object_create(request, config)


def label_update(request, pk):
    config = UpdateConfig(
        model=Label,
        form_class=LabelForm,
        template_name='labels/label_form.html',
        success_url='labels_list',
        success_message=gettext("Label is successfully updated")
    )
    return object_update(request, pk, config)


def label_delete(request, pk):
    config = DeleteConfig(
        model=Label,
        template_name='labels/label_delete.html',
        success_url='labels_list',
        success_message=gettext("Label is successfully deleted"),
        in_use_message=gettext("Cannot delete label because it is in use"),
        related_field='task_set'
    )
    return object_delete(request, pk, config)
