from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema

from teachbase.services import TeachbaseClient
from teachbase.serializers import CourseInputSerializer

from teachbase.tests.mocks import TeachbaseClientMock


@extend_schema(tags=["Teachbase"])
class TeachbaseViewSet(ViewSet):
    """
    Teachbase

    """

    teachbase_client = TeachbaseClient()

    def list(self, request, *args, **kwargs):
        courses = self.teachbase_client.get_courses()
        return Response(data=courses, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        pk = request.data["pk"]
        course_detail = self.teachbase_client.get_course_detail(pk)
        return Response(data=course_detail, status=status.HTTP_200_OK)

    @action(detail=False, methods=("POST",))
    def create_user(self, request, *args, **kwargs):
        user_data = request.data["user"]
        created_user = self.teachbase_client.create_user(user_data)
        return Response(data=created_user, status=status.HTTP_200_OK)

    @action(detail=False, methods=("POST",))
    def register_user(self, request, *args, **kwargs):
        pk = request.data["pk"]
        user_id = request.data["user_id"]
        self.teachbase_client.register_user_in_course_session(pk, user_id)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=("GET",))
    def course_sessions(self, request, *args, **kwargs):
        pk = request.data["pk"]
        course_sessions = self.teachbase_client.get_course_sessions_list(pk)
        return Response(data=course_sessions, status=status.HTTP_200_OK)

    @action(detail=False, methods=("POST",))
    def save_course(self, request, *args, **kwargs):
        pk = request.data["pk"]
        course_detail = self.teachbase_client.get_course_detail(pk)
        print(course_detail)
        serializer = CourseInputSerializer(data=course_detail, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
