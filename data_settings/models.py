from email.policy import default
from django.db import models
from helpers.models import TrackingModel


class OccurrenceType(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_occurrencetype", "can deactivate occurrence type"],
            ["print_occurrencetype", "can print occurrence type"],
            ["import_occurrencetype", "can import occurrence type"],
            ["export_occurrencetype", "can export occurrence type"],
        ]


class InvestigationStatus(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_investigationstatus",
                "can deactivate investigation status",
            ],  # noqa
            ["print_investigationstatus", "can print investigation status"],
            ["import_investigationstatus", "can import investigation status"],
            ["export_investigationstatus", "can export investigation status"],
        ]


class OccurrenceCategory(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_occurrencecategory",
                "can deactivate occurrence category",
            ],  # noqa
            ["print_occurrencecategory", "can print occurrence category"],
            ["import_occurrencecategory", "can import occurrence category"],
            ["export_occurrencecategory", "can export occurrence category"],
        ]


class ReportStatus(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_reportstatus", "can deactivate report status"],
            ["print_reportstatus", "can print report status"],
            ["import_reportstatus", "can import report status"],
            ["export_reportstatus", "can export report status"],
        ]


class HighestInjuryLevel(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_highestinjurylevel",
                "can deactivate highest injury level",
            ],  # noqa
            ["print_highestinjurylevel", "can print highest injury level"],
            ["import_highestinjurylevel", "can import highest injury level"],
            ["export_highestinjurylevel", "can export highest injury level"],
        ]


class TypeOfOperation(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_typeofoperation",
                "can deactivate type of operation",
            ],  # noqa
            ["print_typeofoperation", "can print type of operation"],
            ["import_typeofoperation", "can import type of operation"],
            ["export_typeofoperation", "can export type of operation"],
        ]


class DamageToAirCraft(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_damagetoaircraft", "can deactivate data settings"],
            ["print_damagetoaircraft", "can print data settings"],
            ["import_damagetoaircraft", "can import data settings"],
            ["export_damagetoaircraft", "can export data settings"],
        ]

# API
class AviationStack(TrackingModel, models.Model):

    api_key = models.CharField(max_length=1500, unique=True)
    data_offset = models.IntegerField()
    data_per_page = models.IntegerField()
    is_active = models.BooleanField(default=True)
    # qs = models.CharField(max_length=1500, unique=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_aviationstack", "can deactivate aviationstack"],
            ["print_aviationstack", "can print aviationstack"],
            ["import_aviationstack", "can import aviationstack"],
            ["export_aviationstack", "can export aviationstack"],
        ]

        
class Airlab(TrackingModel, models.Model):

    api_key = models.CharField(max_length=1500, unique=True)
    is_active = models.BooleanField(default=True)
    # qs = models.CharField(max_length=1500, unique=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_airlab", "can deactivate airlab"],
            ["print_airlab", "can print airlab"],
            ["import_airlab", "can import airlab"],
            ["export_airlab", "can export airlab"],
        ]


class APIProvider(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    endpoint = models.CharField(max_length=1500, unique=True)
    access_key = models.CharField(max_length=1500, unique=True)
    is_active = models.BooleanField(default=True)
    # qs = models.CharField(max_length=1500, unique=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_apiprovider", "can deactivate api provider"],
            ["print_apiprovider", "can print api provider"],
            ["import_apiprovider", "can import api provider"],
            ["export_apiprovider", "can export api provider"],
        ]

# LOCATION
class Country(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    capital = models.CharField(max_length=500, blank=True)
    iso = models.CharField(max_length=500, blank=True)
    fisp_code = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_country", "can deactivate country"],
            ["print_country", "can print country"],
            ["import_country", "can import country"],
            ["export_country", "can export country"],
        ]


class State(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    capital = models.CharField(max_length=500, blank=True)
    iso = models.CharField(max_length=500, blank=True)
    fisp_code = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_state", "can deactivate state"],
            ["print_state", "can print state"],
            ["import_state", "can import state"],
            ["export_state", "can export state"],
        ]


class City(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    iata_code = models.CharField(max_length=50, blank=True)
    iso = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_city", "can deactivate city"],
            ["print_city", "can print city"],
            ["import_city", "can import city"],
            ["export_city", "can export city"],
        ]
# END LOCATION


class Airport(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    iata_code = models.CharField(max_length=50, blank=True)
    icao = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    timezone = models.DateTimeField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_airport", "can deactivate airport"],
            ["print_airport", "can print airport"],
            ["import_airport", "can import airport"],
            ["export_airport", "can export airport"],
        ]


class Airplane(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_airplane", "can deactivate airplane"],
            ["print_airplane", "can print airplane"],
            ["import_airplane", "can import airplane"],
            ["export_airplane", "can export airplane"],
        ]


class Airline(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    iata_code = models.CharField(max_length=50, blank=True)
    icao = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(max_length=50, default=True)
    country = models.CharField(max_length=50, blank=True)
    hub_code = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_airline", "can deactivate airline"],
            ["print_airline", "can print airline"],
            ["import_airline", "can import airline"],
            ["export_airline", "can export airline"],
        ]


class Manufacturer(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_manufacturer", "can deactivate manufacturer"],
            ["print_manufacturer", "can print manufacturer"],
            ["import_manufacturer", "can import manufacturer"],
            ["export_manufacturer", "can export manufacturer"],
        ]


class AircraftType(TrackingModel, models.Model):

    name = models.CharField(max_length=500, unique=True)
    iata_code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_aircrafttype", "can deactivate aircraft type"],
            ["print_aircrafttype", "can print aircraft type"],
            ["import_aircrafttype", "can import aircraft type"],
            ["export_aircrafttype", "can export aircraft type"],
        ]


class FlightPhase(TrackingModel, models.Model):
    FLIGHT_PHASES =  [
        ("TAKEOFF", "Takeoff"),
        ("LANDING", "Landing")
    ]

    name = models.CharField(max_length=500, choices=FLIGHT_PHASES,
                  default="PENDING")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ["deactivate_flightphase", "can deactivate flight phase"],
            ["print_flightphase", "can print flight phase"],
            ["import_flightphase", "can import flight phase"],
            ["export_flightphase", "can export flight phase"],
        ]


