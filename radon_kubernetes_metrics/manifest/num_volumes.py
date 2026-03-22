from ..utils import ParsedManifest

class NumVolumes:

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

            volumes = spec.get("volumes", [])
            if isinstance(volumes, list):
                total += len(volumes)

        return total