from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.tags.models import Tag


class TagCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password')
        self.client.login(username='testuser', password='password')

    def test_create_status(self):
        response = self.client.post(
            reverse('tag_create'),
            {'name': 'New Tag'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name='New Tag').exists())

    def test_list_tags(self):
        Tag.objects.create(name='Tag 1')
        Tag.objects.create(name='Tag 2')
        response = self.client.get(reverse('tags_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tag 1')
        self.assertContains(response, 'Tag 2')

    def test_update_tag(self):
        tag = Tag.objects.create(name='Old Tag')
        response = self.client.post(
            reverse('tag_update', args=[tag.id]),
            {'name': 'Updated Tag'})

        self.assertEqual(response.status_code, 302)
        tag.refresh_from_db()
        self.assertEqual(tag.name, 'Updated Tag')

    def test_delete_tag(self):
        tag = Tag.objects.create(name='Tag to Delete')
        response = self.client.post(reverse('tag_delete', args=[tag.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())
