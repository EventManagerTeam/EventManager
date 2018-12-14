from rest_framework.routers import SimpleRouter

from .views import EventViewSet
from .views import CategoriesViewSet
from .views import CommentsViewSet
from .views import InvitationsViewSet
from .views import AccountDetailsViewSet


router = SimpleRouter()
router.register("events", EventViewSet)
router.register("comments", CommentsViewSet)
router.register("categories", CategoriesViewSet)
router.register("invitations", InvitationsViewSet)
router.register("details", AccountDetailsViewSet)

urlpatterns = router.urls
