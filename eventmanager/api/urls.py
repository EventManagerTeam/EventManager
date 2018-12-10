from rest_framework.routers import SimpleRouter

from .views import EventViewSet
from .views import CategoriesViewSet
from .views import CommentsViewSet
from .views import InvitationsViewSet


router = SimpleRouter()
router.register("events", EventViewSet)
router.register("comments", CommentsViewSet)
router.register("categories", CategoriesViewSet)
router.register("invitations", InvitationsViewSet)

urlpatterns = router.urls
