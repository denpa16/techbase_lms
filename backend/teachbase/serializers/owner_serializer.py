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


class OwnerInputSerializer(Serializer):
    """
    Сериализтор входных данных владельца

    """

    name = CharField()
