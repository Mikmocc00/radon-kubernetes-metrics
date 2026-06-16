from ..utils import ParsedManifest
from ..manifest.nested_object_ratio import NestedObjectRatio
from ..manifest.avg_fields_per_resource import AvgFieldsPerResource


class NestingPressure:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        nested_object_ratio = NestedObjectRatio(self.manifest).count()
        avg_fields_per_resource = AvgFieldsPerResource(self.manifest).count()

        return nested_object_ratio * avg_fields_per_resource