from django.contrib.auth.models import User
from rest_framework import serializers

from drawing.models import ROI, Sample, Experiment
from trontheim.viewsets import PublishingViewSet


class RoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROI
        fields = "__all__"

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = "__all__"

class SampleSerializer(serializers.ModelSerializer):
    bioimages =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    representations =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = ("id","location","bioimages","representations","experiment","creator")


