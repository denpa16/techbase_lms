from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet
from courses.models import Course
from courses.serializers import (
    CourseSerializer,
)

@extend_schema(tags=["Courses"])
class CourseViewSet(ReadOnlyModelViewSet):
    """
    Курсы

    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
