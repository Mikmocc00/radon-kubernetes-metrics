from ..utils import ParsedManifest

class NumNodeSelectors:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            spec = doc.get("spec", {})
            if "template" in spec and isinstance(spec["template"], dict):
                spec = spec["template"].get("spec", {})

            node_selector = spec.get("nodeSelector", {})
            if isinstance(node_selector, dict):
                total += len(node_selector)

        return total