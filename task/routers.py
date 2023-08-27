from rest_framework import routers
from task.views import TaskItemViewSet

router = routers.SimpleRouter()
router.register(r'', TaskItemViewSet, basename='tasks')

urlpatterns = router.urls