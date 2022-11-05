from unittest.util import _MAX_LENGTH
from django.db import models
from helpers.models import TrackingModel
from django.utils.translation import gettext as _


class AircraftTemplateManager(TrackingModel, models.Model):

    icao_code = models.CharField(_("ICAO CODE"), max_length=500, blank=True, null=True)
    aircraft_model = models.CharField(_("Aircraft Model"), max_length=500, blank=True, null=True)
    year_manufactured = models.CharField(_("Year of manufacture"), max_length=500, blank=True, null=True)
    model_3d_image = models.ImageField(_("Aircraft Image"), 
        upload_to="model_3d_image//%Y/%m/%d", blank=True, null=True
    )
    type = models.CharField(_("Aircraft Type"), max_length=1500, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=500, blank=True, null=True)
    engine_type = models.CharField(_("Engine Type"), max_length=500, blank=True, null=True)
    engine_count = models.CharField(_("Engine Count"), max_length=500, blank=True, null=True)
    wtc = models.CharField(_("Wake Turbulence Category"), max_length=500, blank=True, null=True)
    iata = models.CharField(_("IATA Code"), max_length=500, blank=True, null=True)
    data_source = models.CharField(_("Source of data"), max_length=500, default="DIRECT") # DIRECT, CSV, API
    is_active = models.BooleanField(_("Active Status"),default=True)


    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_aircrafttemplatemanager",
                "can deactivate aircraft template manager",
            ],
            ["print_aircrafttemplatemanager", "can print aircraft template manager"],
            [
                "import_aircrafttemplatemanager",
                "can import aircraft template manager",
            ],
            [
                "export_aircrafttemplatemanager",
                "can export aircraft template manager",
            ],
        ]

    def __str__(self):
        return self.aircraft_model



class Manufacturer(TrackingModel, models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_manufacturer",
                "can deactivate aircraft manufacturer",
            ],
            ["print_manufacturer", "can print aircraft manufacturer"],
            [
                "import_manufacturer",
                "can import aircraft manufacturer",
            ],
            [
                "export_manufacturer",
                "can export aircraft manufacturer",
            ],
        ]

    def __str__(self):
        return self.name