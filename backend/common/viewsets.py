from http import HTTPStatus
from typing import Any, Type

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet


class SoloModelViewSet(GenericViewSet):
    def list(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        queryset: Type[QuerySet] = self.get_queryset()
        serializer: Type[Serializer] = self.get_serializer(queryset.first())
        data: dict[str, Any] = serializer.data
        return Response(data=data, status=HTTPStatus.OK)
