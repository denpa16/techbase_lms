import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

from teachbase.tests.mocks import TeachbaseClientMock
from courses.models import Course, Author, CourseType, Owner


@pytest.mark.django_db
class TestTeachbaseViewSet:
    """
    Тестирование Teachbase
    """

    def test_save_course(self, api_client, django_assert_max_num_queries):
        """
        Тестирование сохранения курса
        """

        mock = TeachbaseClientMock()
        course_data = mock.get_course()

        url = reverse("teachbase-save-course")
        with patch("teachbase.services.TeachbaseClient.get_course_detail") as mock_post_1:
            mock_post_1.return_value = course_data
            with django_assert_max_num_queries(12):
                response = api_client.post(url, data={"pk": 1})
            assert response.status_code == status.HTTP_200_OK

        courses = Course.objects.all()
        authors = Author.objects.all()
        types = CourseType.objects.all()
        owners = Owner.objects.all()
        assert len(courses) == 1
        assert len(authors) == len(course_data["authors"])
        assert len(types) == len(course_data["types"])
        assert len(owners) == 1
