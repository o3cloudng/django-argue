from email.policy import default
from random import choices

from accounts.models import User
from data_settings.models import (FlightPhase, HighestInjuryLevel,
                                  InvestigationStatus, OccurrenceCategory,
                                  OccurrenceType, State)
from django.db import models
from helpers.models import TrackingModel
from django.db.models.signals import pre_save, post_save

class OccurrenceMetaData(TrackingModel, models.Model):
    STATUS =  [
        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("DISCONTINUED", "Discontinued"),
        ("DEACTIVATED", "Deactivated")
    ]
    PUBLISHED =  [
        ("PENDING", "Pending"),
        ("INTERIM", "Interim"),
        ("PRELIMINARY", "Preliminary"),
        ("FINAL", "Final")
    ]
    title = models.CharField(max_length=200, unique=True)
    report_number = models.CharField(max_length=200, blank=True) # AIB-001-YEAR
    # report_creator = models.ForeignKey(User, related_name="report_creator", on_delete=models.CASCADE)
    # occurrence_category = models.ForeignKey(OccurrenceCategory, related_name="occurrence_category", on_delete=models.CASCADE)
    # occurrence_type = models.ForeignKey(OccurrenceType, related_name="occurrence_type", on_delete=models.CASCADE)
    # state = models.ForeignKey(State, related_name="state", on_delete=models.CASCADE)
    # highest_injury_level = models.ForeignKey(HighestInjuryLevel, related_name="highest_injury_level", on_delete=models.CASCADE)
    # investigation_status = models.ForeignKey(InvestigationStatus, related_name="investigation_status", on_delete=models.CASCADE)
    # flight_phase = models.ForeignKey(FlightPhase, related_name="flight_phase", on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=True)
    departure = models.CharField(max_length=200, blank=True)
    destination = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, choices=STATUS, default="ACTIVE")
    is_active = models.BooleanField(default=True)
    published_status = models.CharField(max_length=200, choices=PUBLISHED, default="PENDING")

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_occurrencemetadata",
                "can deactivate occurrence meta data",
            ],
            ["print_occurrencemetadata", "can print occurrence meta data"],
            [
                "import_occurrencemetadata",
                "can import occurrence meta data",
            ],
            [
                "export_occurrencemetadata",
                "can export occurrence meta data",
            ],
        ]

    def __str__(self):
        return self.title

def report_number_pre_save(sender, instance, *args, **kwargs):
    generate_id = "000001"
    year = 2022
    instance.report_number = "AIB"+generate_id+year
    instance.save()

pre_save.connect(report_number_pre_save, sender=OccurrenceMetaData)




class ReportSection(TrackingModel, models.Model):
    title = models.CharField(max_length=200, unique=True)
    occurrence_report = models.ForeignKey(OccurrenceMetaData, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    published_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_reportsection",
                "can deactivate report section",
            ],
            ["print_reportsection", "can print report section"],
            [
                "import_reportsection",
                "can import report section",
            ],
            [
                "export_reportsection",
                "can export report section",
            ],
        ]

    def __str__(self):
        return self.title


class ReportSubSection(TrackingModel, models.Model):
    title = models.CharField(max_length=200, unique=True)
    report_section = models.ForeignKey(ReportSection, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    published_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            [
                "deactivate_reportsubsection",
                "can deactivate report sub section",
            ],
            ["print_reportsubsection", "can print report sub section"],
            [
                "import_reportsubsection",
                "can import report sub section",
            ],
            [
                "export_reportsubsection",
                "can export report sub section",
            ],
        ]

    def __str__(self):
        return self.title