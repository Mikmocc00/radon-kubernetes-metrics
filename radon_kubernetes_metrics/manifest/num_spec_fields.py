from ..utils import ParsedManifest

class NumSpecFields:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def _count_fields(self, obj):
        if isinstance(obj, dict):
            return sum(self._count_fields(v) for v in obj.values()) + len(obj)
        elif isinstance(obj, list):
            return sum(self._count_fields(i) for i in obj)
        else:
            return 0

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if isinstance(doc, dict) and 'spec' in doc:
                total += self._count_fields(doc['spec'])

        return total