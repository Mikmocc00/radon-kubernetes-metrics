from ..utils import ParsedManifest, all_keys

class ManifestStructuralComplexity:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total_fields = 0
        resource_count = 0

        for doc in self.manifest.docs:
            if not doc:
                continue

            total_fields += len(all_keys(doc))
            resource_count += 1

        return total_fields * resource_count