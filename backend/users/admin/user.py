from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from users.models import User


@register(User)
class UserAdmin(UserAdmin):
    """
    Пользователь
    """
    pass
