from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class BaseLimitOffsetPagination(LimitOffsetPagination):
    """
    Базовая пагинация
    """

    default_limit = 12


class BasePageNumberPagination(PageNumberPagination):
    page_size = 6
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
