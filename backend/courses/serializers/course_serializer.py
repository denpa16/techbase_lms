from rest_framework.serializers import (
    Serializer,
    IntegerField,
    CharField,
    DateTimeField,
    BooleanField,
)
from .author_serializer import AuthorSerializer
from .type_serializer import CourseTypeSerializer


class CourseSerializer(Serializer):
    """
    Сериализатор курса

    """

    name = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    owner_id = IntegerField(source="owner.id")
    owner_name = CharField(source="owner.name")
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
    authors = AuthorSerializer(many=True)
    types = CourseTypeSerializer(many=True)

