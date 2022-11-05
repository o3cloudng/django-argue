from datetime import date

from data_settings.models import (FlightPhase, HighestInjuryLevel,
                                  InvestigationStatus, OccurrenceCategory,
                                  OccurrenceType, State)
from django.db.models import Max
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    # FlightData, FlightDataSerializer, 
    OccurrenceMetaData,
                          OccurrenceMetaDataSerializer, ReportSection,
                          ReportSectionSerializer, ReportSubSection,
                          ReportSubSectionSerializer, 
                        #   Stakeholder, StakeholderSerializer, 
                          OccurrenceMetaDataViewSerializer)


class OccurrenceMetaDataListCreateAPIView(generics.ListCreateAPIView):
    queryset = OccurrenceMetaData.objects.select_related("occurrence_category", "occurrence_type", "state", "highest_injury_level", "investigation_status", "flight_phase").all()
    permission_classes = (IsAuthenticated, )
    serializer_class = OccurrenceMetaDataSerializer

    def list(self, request):
        if not request.user.has_perm("occurence_report.view_occurencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = OccurrenceMetaDataViewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.add_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Report creator must be the current user
        request.data["report_creator"] = request.user.id

        # Get the highest id from the report section increment it by 2 to generate the Report Number
        oid = OccurrenceMetaData.objects.aggregate(Max('id'))
        oid = oid["id__max"] + 2
        generate_id = str(oid).zfill(6)
        year = date.today().year
        request.data["report_number"] = "AIB-"+str(generate_id)+"-"+str(year)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OccurrenceMetaDataDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccurrenceMetaData.objects.select_related("occurrence_category", "occurrence_type", "state", "highest_injury_level", "investigation_status", "flight_phase").all()
    serializer_class = OccurrenceMetaDataViewSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OccurrenceMetaDataSerializer
        else:
            return OccurrenceMetaDataViewSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.view_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.change_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)

        # serializer = OccurrenceMetaDataSerializer(data = request.data)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.delete_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


class ReportSectionListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReportSection.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ReportSectionSerializer

    def list(self, request):
        if not request.user.has_perm("occurence_report.view_occurencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = ReportSectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.add_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)

        # Report creator must be the current user
        request.data["occurrence_owner"] = request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        
        serializer.save()
        print("####  SERIALIZER DATA")
        print(serializer.data["id"])

        if serializer.data:
            ReportSubSection.objects.bulk_create([
                ReportSubSection(title="Executive Summary", report_section=serializer.data, occurrence_manager=request.user),
                ReportSubSection(title="Safety Recommendations", report_section=serializer.data, occurrence_manager=request.user),
                ReportSubSection(title="Similar Occurrence", report_section=serializer.data, occurrence_manager=request.user)
            ])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReportSectionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  ReportSection.objects.all()
    serializer_class = ReportSectionSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.view_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.change_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.delete_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


class ReportSubSectionListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReportSubSection.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ReportSubSectionSerializer

    def list(self, request):
        if not request.user.has_perm("occurence_report.view_occurencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = ReportSubSectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.add_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportSubSectionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  ReportSubSection.objects.all()
    serializer_class = ReportSubSectionSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.view_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.change_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("occurence_report.delete_occurrencereport"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


# class StakeholderListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Stakeholder.objects.all()
#     permission_classes = (IsAuthenticated, )
#     serializer_class = StakeholderSerializer

#     def list(self, request):
#         if not request.user.has_perm("occurence_report.view_occurencereport"):
#             return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
#         queryset = self.get_queryset()
#         serializer = StakeholderSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         if not request.user.has_perm("occurence_report.add_occurrencereport"):
#             return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class StakeholderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset =  Stakeholder.objects.all()
#     serializer_class = StakeholderSerializer
#     permission_classes = (IsAuthenticated, )
#     lookup_field = "id"

#     def get(self, request, *args, **kwargs):
#         if not request.user.has_perm("occurence_report.view_occurrencereport"):
#             return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         if not request.user.has_perm("occurence_report.change_occurrencereport"):
#             return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
#         return super().put(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         if not request.user.has_perm("occurence_report.delete_occurrencereport"):
#             return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
#         return super().delete(request, *args, **kwargs)
