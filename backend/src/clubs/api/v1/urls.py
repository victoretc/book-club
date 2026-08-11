from rest_framework.routers import DefaultRouter

from clubs.api.v1.views import ClubRequestViewSet, ClubViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r"club-requests", ClubRequestViewSet, basename="club-request")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"", ClubViewSet, basename="club")


urlpatterns = router.urls
