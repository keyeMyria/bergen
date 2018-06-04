
from rest_framework import routers
from social.views import UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)