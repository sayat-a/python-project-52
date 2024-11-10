from django.urls import reverse
from django.test import TestCase
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password')
        self.client.login(username='testuser', password='password')

    def test_create_status(self):
        response = self.client.post(
            reverse('status_create'),
            {'name': 'New Status'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_list_statuses(self):
        Status.objects.create(name='Status 1')
        Status.objects.create(name='Status 2')
        response = self.client.get(reverse('statuses_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Status 1')
        self.assertContains(response, 'Status 2')

    def test_update_status(self):
        status = Status.objects.create(name='Old Status')
        response = self.client.post(
            reverse('status_update', args=[status.id]),
            {'name': 'Updated Status'})

        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated Status')

    def test_delete_status(self):
        status = Status.objects.create(name='Status to Delete')
        response = self.client.post(reverse('status_delete', args=[status.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=status.id).exists())
