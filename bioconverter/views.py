from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from bioconverter.models import ConversionRequest, Converter, OutFlower, OutFlowRequest
from bioconverter.serializers import ConversionRequestSerializer, ConverterSerializer, OutFlowerSerializer, \
    OutFlowRequestSerializer
from trontheim.viewsets import PublishingViewSet, channel_layer

class ConverterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Converter.objects.all()
    serializer_class = ConverterSerializer

class OutFlowerViewSet(viewsets.ModelViewSet):

    queryset = OutFlower.objects.all()
    serializer_class = OutFlowerSerializer

class ConversionRequestViewSet(viewsets.ModelViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = ConversionRequest.objects.all()
    serializer_class = ConversionRequestSerializer

    def perform_create(self, serializer):
        request = serializer.save()
        try:
            converteritem = request.converter
            path = str(converteritem.channel)
            async_to_sync(channel_layer.send)(path, {"type": "startconverting", "request": serializer.data})
        except KeyError as e:
            print(e)


class OutFlowRequestViewSet(viewsets.ModelViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = OutFlowRequest.objects.all()
    serializer_class = OutFlowRequestSerializer

    def perform_create(self, serializer):
        request = serializer.save()
        try:
            outfloweritem = request.outflower
            path = str(outfloweritem.channel)
            print(path)
            async_to_sync(channel_layer.send)(path, {"type": "startconverting", "request": serializer.data})
        except KeyError as e:
            print(e)


