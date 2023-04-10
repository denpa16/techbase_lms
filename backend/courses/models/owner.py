from django.db import models


class Owner(models.Model):
    """
    Владелец

    """

    name = models.CharField(
        verbose_name="Название",
        max_length=255,
    )

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"

    def __str__(self):
        return self.name
