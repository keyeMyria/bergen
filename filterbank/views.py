from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action

from filterbank.models import ParsingRequest, Filter, Representation
from filterbank.serializers import ParsingRequestSerializer, FilterSerializer, RepresentationSerializer
from trontheim.viewsets import PublishingViewSet, channel_layer


class FilterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer

class RepresentationViewSet(viewsets.ModelViewSet):

    queryset = Representation.objects.all()
    serializer_class = RepresentationSerializer

    @action(methods=['get'], detail=True,
            url_path='asimage', url_name='asimage')
    def asimage(self, request):
        representation: Representation = self.get_object()
        image_data = representation.image.image
        return HttpResponse(image_data, content_type="image/png")




class ParsingRequestViewSet(viewsets.ModelViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = ParsingRequest.objects.all()
    serializer_class = ParsingRequestSerializer

    def perform_create(self, serializer):
        request = serializer.save()
        try:
            filteritem = request.filter
            path = str(filteritem.channel)
            async_to_sync(channel_layer.send)(path, {"type": "startparsing", "request": serializer.data})
        except KeyError as e:
            print(e)