import yaml
from ..utils import all_keys


class NumTotalFields:

    def __init__(self, script):
        self.script = script

    def count(self):

        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            total += len(all_keys(doc))

        return total