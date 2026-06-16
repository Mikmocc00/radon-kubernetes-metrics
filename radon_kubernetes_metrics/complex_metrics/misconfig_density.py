from ..utils import ParsedManifest
from ..manifest.num_deprecated_api_versions import NumDeprecatedAPIVersions
from ..manifest.num_duplicate_names import NumDuplicateNames
from ..manifest.num_resources import NumResources


class MisconfigDensity:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_resources = NumResources(self.manifest).count()

        if num_resources == 0:
            return 0.0

        num_deprecated_api_versions = NumDeprecatedAPIVersions(self.manifest).count()
        num_duplicate_names = NumDuplicateNames(self.manifest).count()

        return (
            num_deprecated_api_versions +
            num_duplicate_names
        ) / num_resources