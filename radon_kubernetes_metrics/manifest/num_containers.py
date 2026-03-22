from ..utils import ParsedManifest

class NumContainers:

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

            containers = spec.get("containers", [])
            if isinstance(containers, list):
                total += len(containers)

        return total