
from rest_framework import routers
from social.views import UserViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"comments", CommentsViewSet)