import re
from ..utils import ParsedManifest


class NumSuspiciousComments:

    KEYWORDS = [
        "TODO",
        "FIXME",
        "BUG",
        "HACK"
    ]

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):

        total = 0

        for word in self.KEYWORDS:
            total += len(re.findall(word, self.manifest.raw_content, re.IGNORECASE))

        return total