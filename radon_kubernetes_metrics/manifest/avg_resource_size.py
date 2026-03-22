from ..utils import ParsedManifest

class AvgResourceSize:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        resources = self.manifest.raw_content.split('---')

        sizes = [
            len(r.strip().splitlines())
            for r in resources if r.strip()
        ]

        if not sizes:
            return 0

        return int(sum(sizes) / len(sizes))