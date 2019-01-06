from rest_framework.routers import SimpleRouter

from api.views import AccountDetailsViewSet
from api.views import CategoriesViewSet
from api.views import CommentsViewSet
from api.views import EventViewSet
from api.views import InvitationsViewSet
from api.views import TasksViewSet


router = SimpleRouter()
router.register("events", EventViewSet)
router.register("comments", CommentsViewSet)
router.register("categories", CategoriesViewSet)
router.register("invitations", InvitationsViewSet)
router.register("details", AccountDetailsViewSet)
router.register("tasks", TasksViewSet)

urlpatterns = router.urls
