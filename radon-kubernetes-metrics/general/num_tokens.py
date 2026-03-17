import re


class NumTokens:

    def __init__(self, script):
        self.script = script

    def count(self):

        tokens = re.findall(r'\w+', self.script)

        return len(tokens)