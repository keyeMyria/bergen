# Create your views here.
import numpy as np
from django.http import HttpResponse
from oauth2_provider.contrib.rest_framework import permissions, TokenHasScope
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.response import Response

from drawing.models import Sample, ROI, Experiment
from drawing.serializers import SampleSerializer, RoiSerializer, ExperimentSerializer
from filterbank.models import Representation
from filterbank.serializers import RepresentationSerializer

from trontheim.viewsets import PublishingViewSet
from django_filters.rest_framework import DjangoFilterBackend

class SampleViewSet(PublishingViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = ["experiment","creator"]
    filter_fields = ("creator",)

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

class ExperimentViewSet(PublishingViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = ["creator"]
    filter_fields = ("creator",)

class RepresentationViewSet(PublishingViewSet):

    queryset = Representation.objects.all()
    serializer_class = RepresentationSerializer
    filter_backends = (DjangoFilterBackend,)
    publishers = ["sample"]
    filter_fields = ("sample",)

    @action(methods=['get'], detail=True,
            url_path='asimage', url_name='asimage')
    def asimage(self, request, pk):
        representation: Representation = self.get_object()
        image_data = representation.image.image
        response = HttpResponse(image_data, content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(representation.image.image.name)
        return response

    @action(methods=['get'], detail=True,
            url_path='asnifti', url_name='asnifti')
    def asnifti(self, request, pk):
        representation: Representation = self.get_object()
        filepath = representation.nifti.file
        image_data = open(filepath, 'rb')
        response = HttpResponse(image_data, content_type="application/gzip")
        response['Content-Disposition'] = 'inline; filename="johannes.nii.gz"'
        return response


    @action(methods=["get"], detail=False,
            url_path="bysample", url_name="bysample")
    def bysample(self,request):
        return HttpResponse("404")

