import math
import yaml
import re
from collections import Counter
from ..utils import all_values


class ConfigEntropy:

    def __init__(self, script):
        self.script = script

    def count(self):

        docs = yaml.safe_load_all(self.script)

        values = []

        for doc in docs:
            if not doc:
                continue

            values.extend(all_values(doc))

        tokens = []

        for v in values:
            if isinstance(v, str):
                tokens.extend(re.findall(r'\w+', v))
            else:
                tokens.append(str(v))

        if not tokens:
            return 0

        counts = Counter(tokens)
        total = len(tokens)

        entropy = 0
        for c in counts.values():
            p = c / total
            entropy -= p * math.log2(p)

        return entropy