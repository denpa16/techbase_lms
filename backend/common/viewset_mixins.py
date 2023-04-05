from rest_framework.decorators import action
from rest_framework.response import Response


class SpecsFacetsMixin:
    @action(detail=False, methods=("GET",))
    def specs(self, request):
        queryset = self.get_queryset()
        filter = self.filterset_class(request.GET, queryset)
        return Response(filter.specs())

    @action(detail=False, methods=("GET",))
    def facets(self, request):
        queryset = self.get_queryset()
        filter = self.filterset_class(request.GET, queryset)
        return Response(filter.facets())
