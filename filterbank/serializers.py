from django.contrib.auth.models import User
from rest_framework import serializers

from filterbank.models import ParsingRequest, Filter, Representation


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = "__all__"


class ParsingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsingRequest
        fields = "__all__"

class RepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representation
        fields = "__all__"


