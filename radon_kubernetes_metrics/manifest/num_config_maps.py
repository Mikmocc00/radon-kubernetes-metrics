from ..utils import ParsedManifest

class NumConfigMaps:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            if doc.get("kind") == "ConfigMap":
                total += 1

        return total