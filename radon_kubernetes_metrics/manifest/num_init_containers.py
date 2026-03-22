from ..utils import ParsedManifest

class NumInitContainers:

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

            init_containers = spec.get("initContainers", [])
            if isinstance(init_containers, list):
                total += len(init_containers)

        return total