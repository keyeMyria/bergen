
from rest_framework import routers

from drawing.views import RoiViewSet, SampleViewSet
from social.views import UserViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register(r"rois", RoiViewSet)
router.register(r"samples", SampleViewSet)