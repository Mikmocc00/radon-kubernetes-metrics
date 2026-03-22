from ..utils import ParsedManifest

class NumPersistentVolumes:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            kind = doc.get("kind")
            if kind in ["PersistentVolume", "PersistentVolumeClaim"]:
                total += 1

        return total