from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    CharField,
)
from courses.models import Course
from .author_serializer import AuthorSerializer
from .type_serializer import CourseTypeSerializer


class CourseSerializer(ModelSerializer):
    """
    Сериализатор курса

    """

    owner_id = IntegerField(source="onwer.ref_id")
    owner_name = CharField(source="owner.name")
    authors = AuthorSerializer(many=True)
    types = CourseTypeSerializer(many=True)

    class Meta:
        model = Course
        fields = ("__all__", "owner_id", "owner_name", "types", "authors")
        exclude = ("owner",)
