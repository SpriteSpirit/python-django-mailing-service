from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from mailing_service.models import Mailing


class Command(BaseCommand):
    help = 'Создание группы с особыми правами доступа'

    def handle(self, *args, **options):
        # Получаем ContentType для каждой модели
        content_type_mailing = ContentType.objects.get_for_model(Mailing)
        content_type_user = ContentType.objects.get_for_model(User)

        # Определяем права для рассылок и пользователей
        mailing_permissions = (
            ('can_view_mailing', 'View mailing'),
            ('can_off_mailing', 'Change mailing status'),
        )
        user_permissions = (
            ('can_view_user', 'View user'),
            ('can_block_user', 'Block user'),
        )

        # Создаем или получаем группу 'Moderator'
        group, created = Group.objects.get_or_create(name='Moderator')

        # Добавляем права для рассылок
        for codename, name in mailing_permissions:
            permission, created = Permission.objects.get_or_create(
                content_type=content_type_mailing,
                codename=codename,
                defaults={'name': name}
            )
            group.permissions.add(permission)

        # Добавляем права для пользователей
        for codename, name in user_permissions:
            permission, created = Permission.objects.get_or_create(
                content_type=content_type_user,
                codename=codename,
                defaults={'name': name}
            )
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS(f'Группа "{group.name}" успешно создана с необходимыми правами.'))
