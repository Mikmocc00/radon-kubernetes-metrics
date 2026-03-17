import yaml


class MaxSpecDepth:

    def __init__(self, script):
        self.script = script

    def _depth(self, obj, level=0):
        if isinstance(obj, dict):
            return max([self._depth(v, level + 1) for v in obj.values()] + [level])
        elif isinstance(obj, list):
            return max([self._depth(i, level + 1) for i in obj] + [level])
        else:
            return level

    def count(self):
        docs = yaml.safe_load_all(self.script)
        max_depth = 0

        for doc in docs:
            if doc and 'spec' in doc:
                depth = self._depth(doc['spec'])
                max_depth = max(max_depth, depth)

        return max_depth