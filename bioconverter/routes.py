
from rest_framework import routers

from bioconverter.views import ConversionRequestViewSet, ConverterViewSet
from drawing.views import RoiViewSet, SampleViewSet
from filterbank.views import FilterViewSet, ParsingRequestViewSet
from social.views import UserViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register(r"converters", ConverterViewSet)
router.register(r"conversions", ConversionRequestViewSet)