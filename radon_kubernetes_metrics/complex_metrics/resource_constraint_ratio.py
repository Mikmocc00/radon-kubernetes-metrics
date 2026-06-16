from ..utils import ParsedManifest
from ..manifest.num_resource_limits import NumResourceLimits
from ..manifest.num_resources import NumResources


class ResourceConstraintRatio:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_resources = NumResources(self.manifest).count()

        if num_resources == 0:
            return 0.0

        num_resource_limits = NumResourceLimits(self.manifest).count()

        return num_resource_limits / num_resources