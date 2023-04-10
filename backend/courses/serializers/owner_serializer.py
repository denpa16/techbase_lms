from rest_framework.serializers import (
    ModelSerializer,
)
from courses.models import Owner


class OwnerSerializer(ModelSerializer):
    """
    Сериализатор владельца

    """

    class Meta:
        model = Owner
        fields = "__all__"
