import yaml


class NumKinds:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        kinds = set()

        for doc in docs:
            if doc and 'kind' in doc:
                kinds.add(doc['kind'])

        return len(kinds)