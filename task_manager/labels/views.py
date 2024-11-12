from task_manager.labels.models import Label
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.labels.forms import LabelForm
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)
from task_manager.mixins import DeletionCheckMixin


class LabelListView(ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'


class LabelCreateView(SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/label_form.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')
    success_message = _("Label is successfully created")


class LabelUpdateView(SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/label_form.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')
    success_message = _("Label is successfully updated")


class LabelDeleteView(SuccessMessageMixin, DeletionCheckMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Label is successfully deleted")
    error_message = _("Cannot delete label because it is in use")

    def has_dependencies(self, label):
        return label.task_set.exists()
