from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, filters
from rest_framework.response import Response

from data_settings.models import (Airplane, Airport, APIProvider, City,
                                  Country, DamageToAirCraft,
                                  HighestInjuryLevel, InvestigationStatus,
                                  Manufacturer, OccurrenceCategory,
                                  OccurrenceType, ReportStatus, State, FlightPhase, Airplane, 
                                  TypeOfOperation, AircraftType, AviationStack, Airlab )
from data_settings.serializers import (AirplaneSerializer, AirportSerializer,
                                       APIProviderSerializer, CitySerializer,
                                       CountrySerializer,
                                       DamageToAirCraftSerializer,
                                       HighestInjuryLevelSerializer,
                                       InvestigationStatusSerializer,
                                       ManufacturerSerializer,
                                       OccurrenceCategorySerializer,
                                       OccurrenceTypeSerializer,
                                       ReportStatusSerializer, StateSerializer,
                                       FlightPhaseSerializer, TypeOfOperationSerializer,
                                       AircraftTypeSerializer, AviationStackSerializer, AirlabSerializer)

from data_settings.resources import ManufacturerResource
from tablib import Dataset
from django_filters.rest_framework import DjangoFilterBackend
# from accounts.pagination import CustomPageNumberPagination


# OCCURRENCE TYPE
class OccurrenceTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = OccurrenceType.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OccurrenceTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["id","name"]
    search_fields = ["id","name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = OccurrenceTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OccurrenceTypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccurrenceType.objects.all()
    serializer_class = OccurrenceTypeSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


# INVESTIGATION STATUS
class InvestigationStatusListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = InvestigationStatus.objects.all()
    serializer_class = InvestigationStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    search_fields = ['id', 'name']

    def list(self, request):
        if not request.user.has_perm("data_settings.view_investigationstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = InvestigationStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_investigationstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvestigationStatusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvestigationStatus.objects.all()
    serializer_class = InvestigationStatusSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_investigationstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_investigationstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_investigationstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


# OCCURRENCE CATEGORIES
class OccurrenceCategoryListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = OccurrenceCategory.objects.all()
    serializer_class = OccurrenceCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencecategory"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = OccurrenceCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencecategory"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OccurrenceCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccurrenceCategory.objects.all()
    serializer_class = OccurrenceCategorySerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencecategory"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencecategory"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencecategory"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


# REPORT STATUS
class ReportStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReportStatus.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ReportStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_reportstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = ReportStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_reportstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportStatusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportStatus.objects.all()
    serializer_class = ReportStatusSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_reportstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_reportstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_reportstatus"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


# HIGHEST INJURY LEVEL
class HighestInjuryLevelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = HighestInjuryLevel.objects.all()
    serializer_class = HighestInjuryLevelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_highestinjurylevel"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = HighestInjuryLevelSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_highestinjurylevel"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HighestInjuryLevelDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HighestInjuryLevel.objects.all()
    serializer_class = HighestInjuryLevelSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_highestinjurylevel"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_highestinjurylevel"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_highestinjurylevel"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


class TypeOfOperationListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = TypeOfOperation.objects.all()
    serializer_class = TypeOfOperationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_typeofoperation"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = TypeOfOperationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_typeofoperation"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TypeOfOperationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TypeOfOperation.objects.all()
    serializer_class = TypeOfOperationSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_typeofoperation"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_typeofoperation"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_typeofoperation"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


class DamageToAirCraftAPIView(generics.ListCreateAPIView):
    queryset = DamageToAirCraft.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DamageToAirCraftSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_damagetoaircraft"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = DamageToAirCraftSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_damagetoaircraft"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DamageToAirCraftDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DamageToAirCraft.objects.all()
    serializer_class = DamageToAirCraftSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"
    
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_damagetoaircraft"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_damagetoaircraft"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_damagetoaircraft"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)



class APIProviderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = APIProvider.objects.all()
    serializer_class = APIProviderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = APIProviderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class APIProviderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = APIProvider.objects.all()
    serializer_class = APIProviderSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


###### LOCATION
# Country
class CountryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CountryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

# State
class StateListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = StateSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

# City
class CityListCreateAPIView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"
    
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)



class AirportListCreateAPIView(generics.ListCreateAPIView):
    queryset = Airport.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AirportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = AirportSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AirportDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

class AirplaneListCreateAPIView(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AirplaneSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = AirplaneSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AirplaneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


class FlightPhaseListCreateAPIView(generics.ListCreateAPIView):
    queryset = FlightPhase.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = FlightPhaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = FlightPhaseSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FlightPhaseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  FlightPhase.objects.all()
    serializer_class = FlightPhaseSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_foccurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


class ManufacturerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ManufacturerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = ManufacturerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ManufacturerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

@api_view(["POST"])
def aircraft_manufacturer_import(request):
    if not request.user.has_perm("data_settings.import_manufacturer"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        
    aircraft_manufacturer = ManufacturerResource()
    dataset = Dataset()
    # dataset = Dataset(['', 'New book'], headers=['id', 'name'])
    if not request.FILES["aircraft_manufacturer"]:
        return Response({"error":"No file found."})
    new_aircraft_manufacturer = request.FILES["aircraft_manufacturer"]

    imported_data = dataset.load(  # noqa
        new_aircraft_manufacturer.read().decode()  , format="csv"
    )

    result = aircraft_manufacturer.import_data(
        dataset, dry_run=True
    )  # Test the data import

    print(imported_data)
    print(result)

    if not result.has_errors():
    # if imported_data:
        aircraft_manufacturer.import_data(dataset, dry_run=False)  # Actually import now
        return Response({"message": "Data upload was successful."})

    return Response(
        {
            "error": "Data import failed. \n Ensure that the headers and data format are correct."  # noqa
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


class AircraftTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = AircraftType.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AircraftTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = AircraftTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AircraftTypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  AircraftType.objects.all()
    serializer_class = AircraftTypeSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


class AviationStackListCreateAPIView(generics.ListCreateAPIView):
    queryset = AviationStack.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AviationStackSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = AviationStackSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AviationStackDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  AviationStack.objects.all()
    serializer_class = AviationStackSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)


class AirlabListCreateAPIView(generics.ListCreateAPIView):
    queryset = Airlab.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AirlabSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]

    def list(self, request):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = AirlabSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.add_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AirlabDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Airlab.objects.all()
    serializer_class = AirlabSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.view_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.change_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.delete_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("data_settings.deactivate_occurrencetype"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

