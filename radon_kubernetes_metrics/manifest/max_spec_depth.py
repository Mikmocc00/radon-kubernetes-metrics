from ..utils import ParsedManifest

class MaxSpecDepth:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def _depth(self, obj, level=0):
        if isinstance(obj, dict):
            if not obj: return level
            return max([self._depth(v, level + 1) for v in obj.values()] + [level])
        elif isinstance(obj, list):
            if not obj: return level
            return max([self._depth(i, level + 1) for i in obj] + [level])
        else:
            return level

    def count(self):
        max_depth = 0

        for doc in self.manifest.docs:
            if isinstance(doc, dict) and 'spec' in doc:
                depth = self._depth(doc['spec'])
                max_depth = max(max_depth, depth)

        return max_depth