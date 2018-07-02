from rest_framework import serializers

from biouploader.models import BioImage


class BioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioImage
        fields = "__all__"