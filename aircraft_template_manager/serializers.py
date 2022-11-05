from rest_framework import serializers

from .models import AircraftTemplateManager


class AircraftTemplateManagerSerializer(serializers.ModelSerializer):

    model_3d_image = serializers.ImageField(required=False)

    class Meta:
        model = AircraftTemplateManager
        fields = "__all__"
