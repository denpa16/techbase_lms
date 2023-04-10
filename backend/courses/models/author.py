from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from courses.constants import AuthorRole, AuthorType


class Author(models.Model):
    """
    Автор

    """

    name = models.CharField(
        verbose_name="Имя",
        max_length=255,
    )
    last_name = models.CharField(
        verbose_name="Имя",
        max_length=255,
    )
    phone = PhoneNumberField(
        verbose_name="Телефон",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True,
    )
    role_id = models.PositiveIntegerField(
        verbose_name="Роль",
        default=AuthorRole.ROLE_1,
    )
    auth_type = models.PositiveIntegerField(
        verbose_name="Тип",
        default=AuthorType.TYPE_1,
    )
    last_activity_at = models.PositiveBigIntegerField(
        verbose_name="Дата последней активности",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name="Активный",
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name
