# products/management/commands/create_moderators_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from mailing_service.models import Mailing


class Command(BaseCommand):
    help = 'Создание группы с особыми правами доступа'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Mailing)
        permissions = (
            ('can_view_mailing', 'View mailing'),
            ('can_off_mailing', 'Change mailing status'),
            ('can_view_user', 'View users'),
            ('can_block_user', 'Block user'),
        )

        group, created = Group.objects.get_or_create(name='Moderator')
        for codename, name in permissions:
            permission, created = Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename,
                defaults={'name': name}
            )
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS(f'Группа "{group.name}" успешно создана.'))