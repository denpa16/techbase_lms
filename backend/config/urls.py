from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .admin import admin
from .routers import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("api/__debug__/", include(debug_toolbar.urls)),)
