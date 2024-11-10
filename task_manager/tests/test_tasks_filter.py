from django.test import TestCase
from task_manager.users.models import CustomUser
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.filter import TaskFilter


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="user1", password="password")
        self.user2 = CustomUser.objects.create_user(
            username="user2", password="password")

        self.status1 = Status.objects.create(name="Status 1")
        self.status2 = Status.objects.create(name="Status 2")

        self.label1 = Label.objects.create(name="Label 1")
        self.label2 = Label.objects.create(name="Label 2")

        self.task1 = Task.objects.create(
            name="Task 1",
            creator=self.user1,
            executor=self.user2,
            status=self.status1)
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name="Task 2",
            creator=self.user2,
            executor=self.user1,
            status=self.status2)
        self.task2.labels.add(self.label2)

    def test_filter_by_status(self):
        data = {'status': self.status1.id}
        filtered_tasks = TaskFilter(data=data, queryset=Task.objects.all()).qs

        self.assertIn(self.task1, filtered_tasks)
        self.assertNotIn(self.task2, filtered_tasks)

    def test_filter_by_executor(self):
        data = {'executor': self.user1.id}
        filtered_tasks = TaskFilter(data=data, queryset=Task.objects.all()).qs

        self.assertIn(self.task2, filtered_tasks)
        self.assertNotIn(self.task1, filtered_tasks)

    def test_filter_by_labels(self):
        data = {'labels': [self.label1.id]}
        filtered_tasks = TaskFilter(data=data, queryset=Task.objects.all()).qs

        self.assertIn(self.task1, filtered_tasks)

    def test_filter_own_tasks(self):
        self.client.force_login(self.user1)
        data = {'filter_own_tasks': True}
        filtered_tasks = TaskFilter(
            data=data, queryset=Task.objects.all(),
            request=self.client.get('/tasks/', data).wsgi_request).qs

        self.client.force_login(self.user1)
        self.assertIn(self.task1, filtered_tasks)
        self.assertNotIn(self.task2, filtered_tasks)
