import yaml


class NumSpecFields:

    def __init__(self, script):
        self.script = script

    def _count_fields(self, obj):
        if isinstance(obj, dict):
            return sum(self._count_fields(v) for v in obj.values()) + len(obj)
        elif isinstance(obj, list):
            return sum(self._count_fields(i) for i in obj)
        else:
            return 0

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if doc and 'spec' in doc:
                total += self._count_fields(doc['spec'])

        return total