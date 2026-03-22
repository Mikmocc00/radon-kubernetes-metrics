from ..utils import ParsedManifest

class NumServices:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if isinstance(doc, dict) and doc.get("kind") == "Service":
                total += 1

        return total