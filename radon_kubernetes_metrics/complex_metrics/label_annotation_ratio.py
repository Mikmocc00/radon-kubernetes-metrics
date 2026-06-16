from ..utils import ParsedManifest
from ..manifest.num_labels import NumLabels
from ..manifest.num_total_fields import NumTotalFields


class LabelAnnotationRatio:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_labels = NumLabels(self.manifest).count()
        num_total_fields = NumTotalFields(self.manifest).count()

        return num_labels / (num_total_fields + 1)