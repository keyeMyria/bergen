# Create your views here.
import numpy as np
from oauth2_provider.contrib.rest_framework import permissions, TokenHasScope
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.response import Response

from drawing.models import Sample, ROI
from drawing.serializers import SampleSerializer, RoiSerializer
from filterbank.models import Representation
from filterbank.serializers import RepresentationSerializer

from trontheim.viewsets import PublishingViewSet


class SampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    @action(methods=['get'], detail=True,
            url_path='initialrep', url_name='initialrep')
    def set_initialrep(self, request, pk):

        sample: Sample = self.get_object()
        rep: Representation = Representation.objects.create(name="initial of Sample {0}".format(sample.name), creator=request.user, vid=0, sample=sample,
                                      numpy=np.zeros((1024,1024,3)))

        serialized = RepresentationSerializer(rep)
        return Response(serialized.data)


class RoiViewSet(PublishingViewSet):
    queryset = ROI.objects.all()
    serializer_class = RoiSerializer
    publishers = ["sample"]
