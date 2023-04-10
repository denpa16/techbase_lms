import datetime
from rest_framework.serializers import (
    FileField,
    FloatField,
    IntegerField,
    ModelSerializer,
    SerializerMethodField,
    Serializer,
    BooleanField,
    Serializer,
    CharField,
    DictField,
    ListField,
    DateTimeField,
)


class AuthorInputSerializer(Serializer):
    """
    Сериализтор входных данных автора

    """

    email = CharField()
    phone = CharField()
    name = CharField()
    last_name = CharField()
    role_id = IntegerField()
    auth_type = IntegerField()
    last_activity_at = IntegerField()
    is_active = BooleanField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
