from django.contrib.auth.models import User
from rest_framework import serializers

from bioconverter.models import ConversionRequest
from filterbank.models import ParsingRequest, Filter, Representation


class ConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = "__all__"


class ConversionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRequest
        fields = "__all__"


