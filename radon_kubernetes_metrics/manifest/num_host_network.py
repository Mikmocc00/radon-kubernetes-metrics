from ..utils import ParsedManifest

class NumHostNetwork:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            spec = doc.get("spec", {})
            if isinstance(spec, dict) and spec.get("hostNetwork") is True:
                total += 1

        return total