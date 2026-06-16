import math
import re
from collections import Counter
from ..utils import ParsedManifest, all_values


class MisconfigurationPressure:


    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest


    @staticmethod
    def _compute_config_entropy(docs: list) -> float:
        values = []
        for doc in docs:
            if not doc:
                continue
            values.extend(all_values(doc))

        tokens = []
        for v in values:
            if isinstance(v, str):
                tokens.extend(re.findall(r'\w+', v))
            else:
                tokens.append(str(v))

        if not tokens:
            return 0.0

        counts = Counter(tokens)
        total = len(tokens)
        entropy = 0.0
        for c in counts.values():
            p = c / total
            entropy -= p * math.log2(p)

        return entropy


    def count(self):
        num_missing_resources = 0
        num_missing_probes = 0
        num_containers = 0
        num_resources = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            num_resources += 1

            spec = doc.get("spec", {})
            if "template" in spec and isinstance(spec["template"], dict):
                pod_spec = spec["template"].get("spec", {})
            else:
                pod_spec = spec

            if not isinstance(pod_spec, dict):
                continue

            containers = pod_spec.get("containers", [])
            init_containers = pod_spec.get("initContainers", [])

            if not isinstance(containers, list):
                containers = []
            if not isinstance(init_containers, list):
                init_containers = []

            all_containers = containers + init_containers
            num_containers += len(all_containers)

            for c in all_containers:
                if not isinstance(c, dict):
                    continue

                resources = c.get("resources", {})
                if not isinstance(resources, dict):
                    resources = {}

                if not resources.get("limits"):
                    num_missing_resources += 1
                if not resources.get("requests"):
                    num_missing_resources += 1

                if c in containers:
                    if not c.get("livenessProbe"):
                        num_missing_probes += 1
                    if not c.get("readinessProbe"):
                        num_missing_probes += 1

        config_entropy = self._compute_config_entropy(self.manifest.docs)

        numerator = (num_missing_resources + num_missing_probes) * config_entropy
        denominator = max(num_containers + num_resources, 1)

        return numerator / denominator