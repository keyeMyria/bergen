
from rest_framework import routers

from biouploader.views import BioImageViewSet
from drawing.views import RoiViewSet, SampleViewSet
from filterbank.views import FilterViewSet, ParsingRequestViewSet
from social.views import UserViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register(r"bioimages", BioImageViewSet)