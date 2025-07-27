# articles/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from articles.models import Article

class Command(BaseCommand):
    help = 'Creates default groups with permissions'

    def handle(self, *args, **kwargs):
        # Get content type for Article model
        content_type = ContentType.objects.get_for_model(Article)

        # Get all permissions for Article model
        permissions = Permission.objects.filter(content_type=content_type)

        # Create Viewers group with can_view permission
        viewers, created = Group.objects.get_or_create(name='Viewers')
        viewers.permissions.add(
            permissions.get(codename='can_view')
        )

        # Create Editors group with can_view, can_create, can_edit
        editors, created = Group.objects.get_or_create(name='Editors')
        editors.permissions.add(
            permissions.get(codename='can_view'),
            permissions.get(codename='can_create'),
            permissions.get(codename='can_edit'),
        )

        # Admins group gets all permissions
        admins, created = Group.objects.get_or_create(name='Admins')
        admins.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups'))