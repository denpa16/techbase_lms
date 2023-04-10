from django.db.models import IntegerChoices


class ContentType(IntegerChoices):
    """
    Тип контента

    """

    TYPE_1 = 1, "TYPE_1"
    TYPE_2 = 2, "TYPE_2"


class AuthorRole(IntegerChoices):
    """
    Роль автора

    """

    ROLE_1 = 1, "ROLE_1"
    ROLE_2 = 2, "ROLE_2"


class AuthorType(IntegerChoices):
    """
    Тип автора

    """

    TYPE_1 = 1, "TYPE_1"
    TYPE_2 = 2, "TYPE_2"
