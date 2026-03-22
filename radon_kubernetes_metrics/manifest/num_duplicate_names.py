from ..utils import ParsedManifest

class NumDuplicateNames:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        names = []

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            name = doc.get("metadata", {}).get("name")
            if name:
                names.append(name)

        return len(names) - len(set(names))