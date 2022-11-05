from django.urls import path
from occurrence_report.views import (
    OccurrenceMetaDataDetailAPIView,
    OccurrenceMetaDataListCreateAPIView,
    ReportSectionListCreateAPIView,
    ReportSectionDetailAPIView,
    ReportSubSectionListCreateAPIView,
    ReportSubSectionDetailAPIView,

)

urlpatterns = [
    path(
        "",
        OccurrenceMetaDataListCreateAPIView.as_view(),
        name="occurrence-report",
    ),
    path(
        "<int:id>/",
        OccurrenceMetaDataDetailAPIView.as_view(),
        name="occurrence-report-details",
    ),
    path(
        "report-section/",
        ReportSectionListCreateAPIView.as_view(),
        name="report-section",
    ),
    path(
        "report-section/<int:id>/",
        ReportSectionDetailAPIView.as_view(),
        name="report-section-details",
    ),
    path(
        "report-sub-section/",
        ReportSubSectionListCreateAPIView.as_view(),
        name="report-sub-section",
    ),
    path(
        "report-sub-section/<int:id>/",
        ReportSubSectionDetailAPIView.as_view(),
        name="report-sub-section-details",
    ),
]
