# # products/management/commands/create_moderators_group.py
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
#
# class Command(BaseCommand):
#     help = 'Создание группы с особыми правами доступа'
#
#     def handle(self, *args, **options):
#         content_type = ContentType.objects.get_for_model(Product)
#         permissions = (
#             ('can_change_product_publication', 'Change product publication'),
#             ('can_change_description_product', 'Change product description'),
#             ('can_change_category', 'Change product category'),
#         )
#
#         group, created = Group.objects.get_or_create(name='moderator')
#         for codename, name in permissions:
#             permission, created = Permission.objects.get_or_create(
#                 content_type=content_type,
#                 codename=codename,
#                 defaults={'name': name}
#             )
#             group.permissions.add(permission)
#
#         self.stdout.write(self.style.SUCCESS(f'Группа "{group.name}" успешно создана.'))