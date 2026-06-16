from ..utils import ParsedManifest
from ..manifest.num_config_maps import NumConfigMaps
from ..manifest.num_resources import NumResources


class ObservabilityScore:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_resources = NumResources(self.manifest).count()

        if num_resources == 0:
            return 0.0

        num_configmaps = NumConfigMaps(self.manifest).count()

        return num_configmaps / num_resources