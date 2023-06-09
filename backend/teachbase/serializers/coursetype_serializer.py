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


class CourseTypeInputSerializer(Serializer):
    """
    Сериализтор входных данных типа курса

    """

    name = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
