from task_manager.labels.models import Label
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.labels.forms import LabelForm
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)


# Create your views here.
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


class LabelDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Label is successfully deleted")

    def form_valid(self, form):
        if self.get_object().task_set.exists():
            messages.error(
                self.request,
                _("Cannot delete label because it is in use")
            )
            return redirect(self.success_url)
        response = super().form_valid(form)
        return response
