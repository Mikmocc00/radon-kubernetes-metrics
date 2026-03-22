from ..utils import ParsedManifest

class NumKinds:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        kinds = set()

        for doc in self.manifest.docs:
            if isinstance(doc, dict) and 'kind' in doc:
                kinds.add(doc['kind'])

        return len(kinds)