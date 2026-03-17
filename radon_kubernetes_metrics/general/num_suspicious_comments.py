import re


class NumSuspiciousComments:

    KEYWORDS = [
        "TODO",
        "FIXME",
        "BUG",
        "HACK"
    ]

    def __init__(self, script):
        self.script = script

    def count(self):

        total = 0

        for word in self.KEYWORDS:
            total += len(re.findall(word, self.script, re.IGNORECASE))

        return total