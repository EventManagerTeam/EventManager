from rest_framework.routers import SimpleRouter

from api.views import AccountDetailsViewSet
from api.views import CategoriesViewSet
from api.views import CommentsViewSet
from api.views import EventViewSet
from api.views import InvitationsViewSet
from api.views import TasksViewSet


router = SimpleRouter()
router.register("events", EventViewSet, base_name='events')
router.register("comments", CommentsViewSet, base_name='comments')
router.register("categories", CategoriesViewSet, base_name='categories')
router.register("invitations", InvitationsViewSet, base_name='invitations')
router.register("details", AccountDetailsViewSet, base_name='details')
router.register("tasks", TasksViewSet, base_name='tasks')

urlpatterns = router.urls
