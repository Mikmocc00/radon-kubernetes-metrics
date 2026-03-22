from ..utils import ParsedManifest

class NumAnnotations:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            annotations = doc.get("metadata", {}).get("annotations", {})
            if isinstance(annotations, dict):
                total += len(annotations)

        return total