from rest_framework.serializers import (
    ModelSerializer,
)
from courses.models import CourseType


class CourseTypeSerializer(ModelSerializer):
    """
    Сериализатор типа

    """

    class Meta:
        model = CourseType
        fields = "__all__"
