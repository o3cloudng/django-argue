from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from data_settings.models import (
    Airlab,
    AviationStack,
    FlightPhase,
    Manufacturer,
    OccurrenceType,
    InvestigationStatus,
    OccurrenceCategory,
    ReportStatus,
    State,
    HighestInjuryLevel,
    DamageToAirCraft,
    APIProvider,
    Country,
    City,
    Airport,
    Airplane,
    TypeOfOperation,
    AircraftType,
)


class OccurrenceTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=OccurrenceType.objects.all())])
    class Meta:
        model = OccurrenceType
        fields = "__all__"


class InvestigationStatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=InvestigationStatus.objects.all())])
    class Meta:
        model = InvestigationStatus
        fields = "__all__"


class OccurrenceCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=OccurrenceCategory.objects.all())])
    class Meta:
        model = OccurrenceCategory
        fields = "__all__"


class ReportStatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=ReportStatus.objects.all())])
    class Meta:
        model = ReportStatus
        fields = "__all__"


class HighestInjuryLevelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=HighestInjuryLevel.objects.all())])
    class Meta:
        model = HighestInjuryLevel
        fields = "__all__"


class TypeOfOperationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=TypeOfOperation.objects.all())])
    class Meta:
        model = TypeOfOperation
        fields = "__all__"


class DamageToAirCraftSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=DamageToAirCraft.objects.all())])
    class Meta:
        model = DamageToAirCraft
        fields = ["id","name"]

class AviationStackSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(max_length=68)
    data_per_page = serializers.IntegerField()
    data_offset = serializers.IntegerField()
    class Meta:
        model = AviationStack
        fields = ["id","api_key","data_per_page","data_offset","is_active"]

# class AviationStackStatusSerializer(serializers.Serializer):
#     is_active = serializers.BooleanField(default=True)

#     class Meta:
#         fields = ["is_active"]

#     def validate(self, attrs):
        

class AirlabSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(max_length=68)
    class Meta:
        model = Airlab
        fields = ["id","api_key","is_active"]

class APIProviderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=APIProvider.objects.all())])
    access_key = serializers.CharField(max_length=68)
    class Meta:
        model = APIProvider
        fields = ["id","name","access_key","endpoint"]


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=Country.objects.all())])
    class Meta:
        model = Country
        fields = "__all__"

class StateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=State.objects.all())])
    class Meta:
        model = State
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=City.objects.all())])
    class Meta:
        model = City
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=Airport.objects.all())])
    class Meta:
        model = Airport
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=Airplane.objects.all())])
    class Meta:
        model = Airplane
        fields = "__all__"


class FlightPhaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=Manufacturer.objects.all())])
    class Meta:
        model = FlightPhase
        fields = "__all__"


class ManufacturerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=Manufacturer.objects.all())])
    class Meta:
        model = Manufacturer
        fields = "__all__"


class AircraftTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=AircraftType.objects.all())])
    iata_code = serializers.CharField(max_length=100)
    class Meta:
        model = AircraftType
        fields = "__all__"
