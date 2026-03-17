import math
from collections import Counter
import re


class TextEntropy:

    def __init__(self, script):
        self.script = script

    def count(self):

        tokens = re.findall(r'\w+', self.script)

        if not tokens:
            return 0

        counts = Counter(tokens)

        total = len(tokens)

        entropy = 0

        for c in counts.values():

            p = c / total
            entropy -= p * math.log2(p)

        return entropy