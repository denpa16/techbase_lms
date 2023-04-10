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

    ref_id = CharField(source="id")
    name = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    owner_id = IntegerField()
    owner_name = CharField()
    thumb_url = CharField()
    cover_url = CharField()
    description = CharField()
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

    @staticmethod
    def get_last_activity(obj):
        return datetime.fromtimestamp(obj.last_activity)

    def create(self, validated_data):
        authors_data = validated_data.pop("authors_set")
        coursetypes_data = validated_data.pop("coursetypes_set")
        owner = Owner.objects.get_or_create(
            ref_id=validated_data.pop("owner_id"),
            name=validated_data.pop("owner_name"),
        )
        course = Course.objects.get_or_create(owner=owner, **validated_data)

        authors = list()
        for author_data in authors_data:
            author = Author.objects.get_or_create(**author_data)
            authors.append(author)
        course.authors.set(authors)

        coursetypes = list()
        for coursetype_data in coursetypes_data:
            coursetype = CourseType.objects.get_or_create(**coursetype_data)
            coursetypes.append(coursetype)
        course.types.set(coursetypes)
