from django.urls import reverse
from django.test import TestCase
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password')
        self.client.login(username='testuser', password='password')

    def test_create_status(self):
        response = self.client.post(
            reverse('label_create'),
            {'name': 'New Label'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_list_labels(self):
        Label.objects.create(name='Label 1')
        Label.objects.create(name='Label 2')
        response = self.client.get(reverse('labels_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Label 1')
        self.assertContains(response, 'Label 2')

    def test_update_label(self):
        label = Label.objects.create(name='Old Label')
        response = self.client.post(
            reverse('label_update', args=[label.id]),
            {'name': 'Updated Label'})

        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, 'Updated Label')

    def test_delete_label(self):
        label = Label.objects.create(name='Label to Delete')
        response = self.client.post(reverse('label_delete', args=[label.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=label.id).exists())
