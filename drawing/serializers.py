from django.contrib.auth.models import User
from rest_framework import serializers

from drawing.models import ROI, Sample


class RoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROI
        fields = "__all__"



class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"
