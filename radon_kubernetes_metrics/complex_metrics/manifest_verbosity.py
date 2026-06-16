from ..utils import ParsedManifest, all_keys


class ManifestVerbosity:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_total_fields = 0
        num_resources = 0
        kinds = set()

        for doc in self.manifest.docs:
            if not doc:
                continue

            num_resources += 1
            num_total_fields += len(all_keys(doc))

            if isinstance(doc, dict):
                kind = doc.get("kind")
                if kind:
                    kinds.add(kind)

        num_kinds = len(kinds)
        denominator = max(num_resources * num_kinds, 1)

        return num_total_fields / denominator