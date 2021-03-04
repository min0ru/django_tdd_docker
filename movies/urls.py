from rest_framework.routers import SimpleRouter

from .views import MovieViewSet

router = SimpleRouter()
router.register("api/movies", MovieViewSet)
urlpatterns = router.urls
