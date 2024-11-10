from django.db import models
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=False)
    status = models.ForeignKey(Status, blank=False, on_delete=models.PROTECT)
    executor = models.ForeignKey(
        CustomUser, blank=False, on_delete=models.PROTECT
    )
    labels = models.ManyToManyField(Label, blank=True)
    creator = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
