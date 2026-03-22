import re
from ..utils import ParsedManifest

class NumTokens:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):

        tokens = re.findall(r'\w+', self.manifest.raw_content)

        return len(tokens)