
from rest_framework import routers

from drawing.views import RoiViewSet, SampleViewSet, ExperimentViewSet, RepresentationViewSet
from social.views import UserViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register(r"rois", RoiViewSet)
router.register(r"samples", SampleViewSet)
router.register(r"experiments", ExperimentViewSet)
router.register(r"representations", RepresentationViewSet)