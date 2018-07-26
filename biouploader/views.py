from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from biouploader.models import BioImage
from biouploader.serializers import BioImageSerializer
from trontheim.viewsets import OsloViewSet


class BioImageViewSet(OsloViewSet):

    queryset = BioImage.objects.all()
    serializer_class = BioImageSerializer
    publishers = [["creator"],"love"]