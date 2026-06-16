from ..utils import ParsedManifest


class SchedulingComplexity:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_affinity_rules = 0
        num_tolerations = 0
        num_node_selectors = 0
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

            affinity = pod_spec.get("affinity", {})
            if isinstance(affinity, dict):
                for affinity_type in ("nodeAffinity", "podAffinity", "podAntiAffinity"):
                    af = affinity.get(affinity_type, {})
                    if not isinstance(af, dict):
                        continue
                    for rule_group in (
                        "requiredDuringSchedulingIgnoredDuringExecution",
                        "preferredDuringSchedulingIgnoredDuringExecution",
                    ):
                        rules = af.get(rule_group, [])
                        if isinstance(rules, list):
                            num_affinity_rules += len(rules)

            tolerations = pod_spec.get("tolerations", [])
            if isinstance(tolerations, list):
                num_tolerations += len(tolerations)

            node_selector = pod_spec.get("nodeSelector", {})
            if isinstance(node_selector, dict):
                num_node_selectors += len(node_selector)

        numerator = num_affinity_rules + num_tolerations + num_node_selectors
        denominator = max(num_resources, 1)

        return numerator / denominator