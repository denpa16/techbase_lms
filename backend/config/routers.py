from rest_framework.routers import DefaultRouter

from courses.viewsets import CourseViewSet
from teachbase.viewsets import TeachbaseViewSet

router = DefaultRouter()

router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"teachbase", TeachbaseViewSet, basename="teachbase")

urlpatterns = router.urls
