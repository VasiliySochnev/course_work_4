from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from auth_users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "manager1@mail.ru"
        password = "manager"
        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        user.is_staff = True
        users_group, created = Group.objects.get_or_create(name="Менеджеры")
        user.groups.add(users_group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Пользователь добавлен в группу "Менеджеры"\nemail для входа: {email}\nпароль: {password}'
            )
        )
