from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.tags.models import Tag


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=False)
    status = models.ForeignKey(Status, blank=False, on_delete=models.PROTECT)
    executor = models.ForeignKey(User, blank=False, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
