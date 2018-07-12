
from rest_framework import routers

from bioconverter.views import ConversionRequestViewSet, ConverterViewSet, OutFlowerViewSet, OutFlowRequestViewSet
from drawing.views import RoiViewSet, SampleViewSet
from filterbank.views import FilterViewSet, ParsingRequestViewSet
from social.views import UserViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register(r"converters", ConverterViewSet)
router.register(r"conversions", ConversionRequestViewSet)
router.register(r"outflower", OutFlowerViewSet)
router.register(r"outflowrequest", OutFlowRequestViewSet)