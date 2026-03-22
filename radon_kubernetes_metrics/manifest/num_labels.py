from ..utils import ParsedManifest

class NumLabels:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            labels = doc.get("metadata", {}).get("labels", {})
            if isinstance(labels, dict):
                total += len(labels)

        return total