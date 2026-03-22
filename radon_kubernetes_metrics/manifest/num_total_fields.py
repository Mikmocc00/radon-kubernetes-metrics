from ..utils import ParsedManifest, all_keys

class NumTotalFields:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not doc:
                continue

            total += len(all_keys(doc))

        return total