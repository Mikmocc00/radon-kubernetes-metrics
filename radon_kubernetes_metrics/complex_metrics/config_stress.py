from ..utils import ParsedManifest
from .structural_density import StructuralDensity
from .misconfig_density import MisconfigDensity
from ..manifest.config_entropy import ConfigEntropy


class ConfigStress:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        structural_density = StructuralDensity(self.manifest).count()
        config_entropy = ConfigEntropy(self.manifest).count()
        misconfig_density = MisconfigDensity(self.manifest).count()

        return (
            structural_density *
            config_entropy *
            (1 + misconfig_density)
        )