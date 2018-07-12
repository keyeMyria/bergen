from django.contrib.auth.models import User
from rest_framework import serializers

from bioconverter.models import ConversionRequest, OutFlowRequest, Converter, OutFlower
from filterbank.models import ParsingRequest, Filter, Representation


class ConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Converter
        fields = "__all__"


class ConversionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRequest
        fields = "__all__"

class OutFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutFlower
        fields = "__all__"

class OutFlowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutFlowRequest
        fields = "__all__"




