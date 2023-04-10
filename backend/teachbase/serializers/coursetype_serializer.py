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

    ref_id = CharField(source="id")
    name = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
