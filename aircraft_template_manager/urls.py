from django.urls import path
from aircraft_template_manager.views import (
    AircraftTemplateManagerListCreateAPIView,
    AircraftTemplateManagerDetailAPIView,
    aircraft_template_manager_import,
    aircraft_template_manager_api_import,
)

urlpatterns = [
    path(
        "", AircraftTemplateManagerListCreateAPIView.as_view(), name="aircaft_template"
    ),
    path(
        "<int:id>/",
        AircraftTemplateManagerDetailAPIView.as_view(),
        name="aircaft_template",
    ),
    path(
        "import/",
        aircraft_template_manager_import,
        name="import_aircraft_template_data",
    ),
    path(
        "api_import/",
        aircraft_template_manager_api_import,
        name="import_aircraft_template_data_api",
    ),
]
