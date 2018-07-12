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