from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserCRUDTests(TestCase):
    fixtures = ['task_manager/tests/users/fixtures/users_fixture.json']

    def setUp(self):
        self.create_url = reverse('signup')
        self.update_url = reverse('user_update', args=[1])
        self.delete_url = reverse('user_delete', args=[1])
        self.login_url = reverse('login')
        self.User = get_user_model()

    def test_user_registration(self):
        """Тест регистрации пользователя (Create)"""
        response = self.client.post(self.create_url, {
            'first_name': 'Vasya',
            'last_name': 'Vasechkin',
            'username': 'Vasyan',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.User.objects.filter(username='Vasyan').exists())

    def test_user_update(self):
        """Тест обновления пользователя (Update)"""
        login = self.client.login(username='testuser', password='password')
        self.assertTrue(login)

        response = self.client.post(self.update_url, {
            'first_name': 'Petr',
            'last_name': 'Sidorov',
            'username': 'testuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })

        self.assertEqual(response.status_code, 302)
        user = self.User.objects.get(pk=1)
        self.assertEqual(user.first_name, 'Petr')

    def test_user_deletion(self):
        """Тест удаления пользователя (Delete)"""
        login = self.client.login(username='testuser', password='password')
        self.assertTrue(login)
        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.User.objects.filter(pk=1).exists())