import math
from collections import Counter
import re
from ..utils import ParsedManifest

class TextEntropy:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):

        tokens = re.findall(r'\w+', self.manifest.raw_content)

        if not tokens:
            return 0

        counts = Counter(tokens)

        total = len(tokens)

        entropy = 0

        for c in counts.values():

            p = c / total
            entropy -= p * math.log2(p)

        return entropy