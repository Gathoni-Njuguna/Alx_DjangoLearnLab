from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from .models import Article

class PermissionTests(TestCase):
    def setUp(self):
        # Create test users
        self.admin = User.objects.create_user(
            username='admin', password='testpass123')
        self.editor = User.objects.create_user(
            username='editor', password='testpass123')
        self.viewer = User.objects.create_user(
            username='viewer', password='testpass123')

        # Assign groups
        admin_group = Group.objects.get(name='Admins')
        editor_group = Group.objects.get(name='Editors')
        viewer_group = Group.objects.get(name='Viewers')

        self.admin.groups.add(admin_group)
        self.editor.groups.add(editor_group)
        self.viewer.groups.add(viewer_group)

        # Create test article
        self.article = Article.objects.create(
            title='Test Article',
            content='Test Content',
            author=self.admin
        )

    def test_view_permissions(self):
        self.client.login(username='viewer', password='testpass123')
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_permissions(self):
        self.client.login(username='viewer', password='testpass123')
        response = self.client.get(reverse('article_create'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='editor', password='testpass123')
        response = self.client.get(reverse('article_create'))
        self.assertEqual(response.status_code, 200)

    def test_edit_permissions(self):
        self.client.login(username='viewer', password='testpass123')
        response = self.client.get(reverse('article_edit', args=[self.article.pk]))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='editor', password='testpass123')
        response = self.client.get(reverse('article_edit', args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_permissions(self):
        self.client.login(username='editor', password='testpass123')
        response = self.client.get(reverse('article_delete', args=[self.article.pk]))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('article_delete', args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)