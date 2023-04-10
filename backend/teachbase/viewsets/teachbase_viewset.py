from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema

from teachbase.services import TeachbaseClient
from teachbase.serializers import CourseInputSerializer


@extend_schema(tags=["Teachbase"])
class TeachbaseViewSet(viewsets.ViewSet):
    """
    Teachbase

    """

    teachbase_client = TeachbaseClient()

    def list(self, request):
        courses = self.teachbase_client.get_courses()
        return Response(data=courses, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        course_detail = self.teachbase_client.get_course_detail(pk)
        return Response(data=course_detail, status=status.HTTP_200_OK)

    def create(self, request):
        user_data = request.data
        created_user = self.teachbase_client.create_user(user_data)
        return Response(data=created_user, status=status.HTTP_200_OK)

    @action(detail=True, methods=("POST",))
    def register_user(self, request, pk=None):
        user_id = request.data.get("user_id")
        self.teachbase_client.register_user_in_course_session(pk, user_id)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=("GET",))
    def course_sessions(self, request, pk=None):
        course_sessions = self.teachbase_client.get_course_sessions_list(pk)
        return Response(data=course_sessions, status=status.HTTP_200_OK)

    @action(detail=True, methods=("POST",))
    def save_course(self, request, pk=None):
        course_detail = self.teachbase_client.get_course_detail(pk)
        serializer = CourseInputSerializer(data=course_detail)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
