from ..utils import ParsedManifest
from ..manifest.manifest_structural_complexity import ManifestStructuralComplexity
from ..manifest.num_kinds import NumKinds


class ManifestComplexityRatio:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_kinds = NumKinds(self.manifest).count()

        if num_kinds == 0:
            return 0.0

        manifest_structural_complexity = ManifestStructuralComplexity(self.manifest).count()

        return manifest_structural_complexity / num_kinds