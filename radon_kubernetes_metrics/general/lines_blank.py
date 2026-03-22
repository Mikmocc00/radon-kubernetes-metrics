from ..utils import ParsedManifest

class LinesBlank:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):

        lines = self.manifest.raw_content.splitlines()

        blank = [l for l in lines if l.strip() == ""]

        return len(blank)