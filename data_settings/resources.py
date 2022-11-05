from import_export import resources
from data_settings.models import Manufacturer


class ManufacturerResource(resources.ModelResource):
    class Meta:
        model = Manufacturer
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'name',)