import yaml

class NumResources:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = list(yaml.safe_load_all(self.script))
        return len([d for d in docs if d is not None])