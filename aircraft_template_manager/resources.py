from import_export import resources
from aircraft_template_manager.models import AircraftTemplateManager


class AircraftTemplateManagerResource(resources.ModelResource):
    class Meta:
        model = AircraftTemplateManager
        skip_unchanged = True
        fields = ("id","icao_code", "aircraft_model", "year_manufactured", 
        "model_3d_image","type","description","engine_type","engine_count","wtc","iata", )
