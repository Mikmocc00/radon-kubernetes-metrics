from ..utils import ParsedManifest

class LinesComment:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):

        lines = self.manifest.raw_content.splitlines()

        comments = [
            l for l in lines
            if l.strip().startswith("#")
               or l.strip().startswith("//")
        ]

        return len(comments)