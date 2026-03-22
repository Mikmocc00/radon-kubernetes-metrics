from ..utils import ParsedManifest

class LinesCode:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):

        lines = self.manifest.raw_content.splitlines()

        code_lines = [
            l for l in lines
            if l.strip() != "" and not l.strip().startswith("#") and not l.strip().startswith("//")
        ]

        return len(code_lines)