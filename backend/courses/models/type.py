from django.db import models


class CourseType(models.Model):
    """
    Тип

    """

    ref_id = models.CharField(
        verbose_name="Внешний  ID",
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name="Название",
        max_length=255,
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
        verbose_name = "Тип курса"
        verbose_name_plural = "Типы курса"

    def __str__(self):
        return self.name
