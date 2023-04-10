from datetime import datetime
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
from courses.models import Owner, Author, CourseType, Course
from .author_serializer import AuthorInputSerializer
from .coursetype_serializer import CourseTypeInputSerializer


class CourseInputSerializer(Serializer):
    """
    Сериализтор входных данных курса

    """

    name = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    owner_name = CharField()
    thumb_url = CharField(allow_blank=True)
    cover_url = CharField(allow_blank=True)
    description = CharField()
    last_activity = CharField(allow_blank=True)
    total_score = IntegerField()
    total_tasks = IntegerField()
    unchangeable = BooleanField()
    include_weekly_report = BooleanField()
    content_type = IntegerField()
    is_netology = BooleanField()
    bg_url = CharField()
    video_url = CharField()
    demo = BooleanField()
    custom_author_names = CharField()
    custom_contents_link = CharField()
    hide_viewer_navigation = BooleanField()
    duration = IntegerField()

    authors = AuthorInputSerializer(many=True)
    types = CourseTypeInputSerializer(many=True)

    def create(self, validated_data):
        authors_data = validated_data.pop("authors")
        coursetypes_data = validated_data.pop("types")
        owner_data = validated_data.pop("owner_name")
        try:
            owner = Owner.objects.get(name=owner_data)
        except Owner.DoesNotExist:
            owner = Owner.objects.create(name=owner_data)
        try:
            course = Course.objects.get(owner=owner, **validated_data)
        except Course.DoesNotExist:
            course = Course.objects.create(owner=owner, **validated_data)

        print(course)

        for author_data in authors_data:
            try:
                author = Author.objects.get(**author_data)
            except Author.DoesNotExist:
                author = Author.objects.create(**author_data)
            course.authors.add(author)

        for coursetype_data in coursetypes_data:
            try:
                coursetype = CourseType.objects.get(**coursetype_data)
            except CourseType.DoesNotExist:
                coursetype = CourseType.objects.create(**coursetype_data)
            course.types.add(coursetype)

        course.save()

        return course
