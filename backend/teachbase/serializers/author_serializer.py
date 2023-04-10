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

    ref_id = CharField(source="id")
    email = CharField()
    phone = CharField()
    name = CharField()
    last_name = CharField()
    role = IntegerField(source="role_id")
    auth_type = IntegerField()
    last_activity = SerializerMethodField()
    is_active = BooleanField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
