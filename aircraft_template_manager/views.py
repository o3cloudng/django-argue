import requests
from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from import_export import resources
from tablib import Dataset
from yaml import serialize

from aircraft_template_manager.models import AircraftTemplateManager
from aircraft_template_manager.resources import AircraftTemplateManagerResource

from data_settings.models import APIProvider
from data_settings.serializers import APIProviderSerializer

from .serializers import AircraftTemplateManagerSerializer
import datetime


# #####  ROLES
class AircraftTemplateManagerListCreateAPIView(generics.ListCreateAPIView):
    queryset = AircraftTemplateManager.objects.all()
    serializer_class = AircraftTemplateManagerSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if not request.user.has_perm("aircraft_template_manager.view_aircrafttemplatemanager"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.get_queryset()
        serializer = AircraftTemplateManagerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("aircraft_template_manager.add_aircrafttemplatemanager"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AircraftTemplateManagerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):  # noqa
    queryset = AircraftTemplateManager.objects.all()
    serializer_class = AircraftTemplateManagerSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("aircraft_template_manager.view_aircrafttemplatemanager"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("aircraft_template_manager.change_aircrafttemplatemanager"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("aircraft_template_manager.delete_aircrafttemplatemanager"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


@api_view(["POST"])
def aircraft_template_manager_import(request):
    if not request.user.has_perm("aircraft_template_manager.import_aircrafttemplatemanager"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        
    aircraft_template_manager = AircraftTemplateManagerResource()
    dataset = Dataset()
    if not request.FILES["aircraft_template_manager"]:
        return Response({"error":"No file found."})
    new_aircraft_template_manager = request.FILES["aircraft_template_manager"]

    imported_data = dataset.load(  # noqa
        new_aircraft_template_manager.read().decode(), format="csv"
    )

    result = aircraft_template_manager.import_data(
        dataset, dry_run=True
    )  # Test the data import
    if not result.has_errors():
    # if imported_data:
        aircraft_template_manager.import_data(dataset, dry_run=False)  # Actually import now
        return Response({"message": "Data upload was successful."})
    return Response(
        {
            "error": "Data import failed. \n Ensure that the headers and data format are correct."  # noqa
        },
        status=status.HTTP_400_BAD_REQUEST,
    )

@api_view(["POST"])
def aircraft_template_manager_api_import(request):
    if not request.user.has_perm("aircraft_template_manager.import_aircrafttemplatemanager"):
        return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)

    provider = str(request.data["provider"])
    limit = str(request.data["limit"])
    # offset = str(request.data["offset"])

    offset_count = AircraftTemplateManager.objects.filter(source="API").count()

    if not limit:
        return Response({"error": "API endpoint not dpecified."}, status=status.HTTP_400_BAD_REQUEST)

    provider = APIProvider.objects.get(name=provider)

    url = provider.endpoint+"airplanes?access_key="+provider.access_key+"&limit="+limit+"1&offset="+offset_count+""
    
    response = requests.get(url)
    data = response.json()

    api = data['data']

    current_year = datetime.datetime.now().year
    for i in api:
        api_data = AircraftTemplateManager(
            source = "API",
            iata = i['iata_type'],
            icao_code = i['icao_code_hex'],
            year_manufactured = (current_year - int(i['plane_age'])),
            aircraft_model = i['model_name'],
            type = i['plane_series'],
            engine_type = i['engines_type'],
            engine_count = i['engines_count'],
            description = i['production_line']
        )
        api_data.save()
        from_api = AircraftTemplateManager.objects.filter(source="API").count()

        # return Response({"api_import_count": from_api}, status=status.HTTP_201_CREATED)
    return Response({"error":"API import failed."},
        status=status.HTTP_400_BAD_REQUEST,
    )
