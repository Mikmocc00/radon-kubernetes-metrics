from ..utils import ParsedManifest
from ..manifest.num_affinity_rules import NumAffinityRules
from ..manifest.num_node_selectors import NumNodeSelectors
from ..manifest.num_tolerations import NumTolerations
from ..manifest.num_resources import NumResources


class SchedulingComplexity:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_resources = NumResources(self.manifest).count()

        if num_resources == 0:
            return 0.0

        num_affinity_rules = NumAffinityRules(self.manifest).count()
        num_node_selectors = NumNodeSelectors(self.manifest).count()
        num_tolerations = NumTolerations(self.manifest).count()

        return (
            num_affinity_rules +
            num_node_selectors +
            num_tolerations
        ) / num_resources