from ..utils import ParsedManifest
from ..manifest.config_entropy import ConfigEntropy
from ..manifest.nested_object_ratio import NestedObjectRatio


class FieldEntropy:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        config_entropy = ConfigEntropy(self.manifest).count()
        nested_object_ratio = NestedObjectRatio(self.manifest).count()

        return config_entropy * nested_object_ratio