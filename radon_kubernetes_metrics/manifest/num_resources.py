from ..utils import ParsedManifest

class NumResources:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        return len([d for d in self.manifest.docs if d is not None])