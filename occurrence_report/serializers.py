from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from data_settings.models import HighestInjuryLevel, OccurrenceCategory
from data_settings.serializers import FlightPhaseSerializer, HighestInjuryLevelSerializer, InvestigationStatusSerializer, OccurrenceCategorySerializer, OccurrenceTypeSerializer, StateSerializer

from occurrence_report.models import (
    OccurrenceMetaData, ReportSection, ReportSubSection, 
    # Stakeholder, FlightData,
)

class OccurrenceMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccurrenceMetaData
        fields = "__all__"

class OccurrenceMetaDataViewSerializer(serializers.ModelSerializer):
    occurrence_category = OccurrenceCategorySerializer()
    occurrence_type = OccurrenceTypeSerializer()
    state = StateSerializer()
    highest_injury_level = HighestInjuryLevelSerializer()
    investigation_status = InvestigationStatusSerializer()
    flight_phase = FlightPhaseSerializer()

    class Meta:
        model = OccurrenceMetaData
        fields = "__all__"
    # def get_occurrence_category(self):
    #     return self.OccurrenceCategory.objects.get(id=)

class ReportSectionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    # slug = serializers.CharField(max_length=100, write_only=True)
    class Meta:
        model = ReportSection
        fields = "__all__"

class ReportSubSectionSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(max_length=100)
    class Meta:
        model = ReportSubSection
        fields = "__all__"

# class StakeholderSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(max_length=100)
#     class Meta:
#         model = Stakeholder
#         fields = "__all__"

# class FlightDataSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(max_length=100)
#     class Meta:
#         model = FlightData
#         fields = "__all__"
