from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status


class TaskCRUDTests(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='user1', password='password')
        self.user2 = CustomUser.objects.create_user(
            username='user2', password='password')
        self.status = Status.objects.create(name='In Progress')
        self.client.login(username='user1', password='password')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            executor=self.user2,
            creator=self.user1
        )

    def test_create_task(self):
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Task Description',
            'status': self.status.id,
            'executor': self.user2.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_list(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_detail(self):
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)

    def test_update_task(self):
        response = self.client.post(
            reverse('task_update', args=[self.task.id]),
            {
                'name': 'Updated Task Name',
                'description': 'Updated Description',
                'status': self.status.id,
                'executor': self.user2.id
            })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task Name')

    def test_delete_task(self):
        response = self.client.post(
            reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_not_creator(self):
        self.client.login(username='user2', password='password')
        response = self.client.post(
            reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
