from django.db import models

from courses.constants import ContentType


class Course(models.Model):
    """
    Курс

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
    owner = models.ForeignKey(
        "courses.Owner",
        verbose_name="Владелец",
        on_delete=models.CASCADE,
    )
    thumb_url = models.URLField(
        verbose_name="URL превью",
        blank=True,
        null=True,
    )
    cover_url = models.URLField(
        verbose_name="URL обложки",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    last_activity = models.DateTimeField(
        verbose_name="Дата последней активности",
        blank=True,
        null=True,
    )
    total_score = models.FloatField(
        verbose_name="Общая оценка",
        default=0,
    )
    total_tasks = models.PositiveIntegerField(
        verbose_name="Общее количество задач",
        default=0,
    )
    unchangeable = models.BooleanField(
        verbose_name="Неизменяемо",
        default=False,
    )
    include_weekly_report = models.BooleanField(verbose_name="Включен в еженедельный отчет")
    content_type = models.CharField(
        verbose_name="Тип контента",
        max_length=32,
        choices=ContentType.choices,
    )
    is_netology = models.BooleanField(
        verbose_name="Нетология",
        default=False,
    )
    bg_url = models.URLField(
        verbose_name="URL заставка",
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        verbose_name="URL видео",
        blank=True,
        null=True,
    )
    demo = models.BooleanField(
        verbose_name="Демо",
        default=False,
    )
    custom_author_names = models.TextField(
        verbose_name="Имена авторов",
        blank=True,
        null=True,
    )
    authors = models.ManyToManyField(
        "courses.Author", verbose_name="Авторы", blank=True, null=True, related_name="authors"
    )
    types = models.ManyToManyField(
        "courses.CourseType",
        verbose_name="Типы",
        blank=True,
        null=True,
        related_name="types",
    )
    custom_contents_link = models.URLField(verbose_name="URL катсомного контента")
    hide_viewer_navigation = models.BooleanField(
        verbose_name="Скрыть навигацию для просмотра",
        default=True,
    )
    duration = models.PositiveIntegerField(
        verbose_name="Длительность",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name
