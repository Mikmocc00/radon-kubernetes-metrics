from ..utils import ParsedManifest

class NumIngresses:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            if doc.get("kind") == "Ingress":
                total += 1

        return total