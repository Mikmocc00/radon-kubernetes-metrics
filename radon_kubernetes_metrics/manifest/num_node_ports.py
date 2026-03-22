from ..utils import ParsedManifest

class NumNodePorts:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            if doc.get("kind") == "Service":
                spec = doc.get("spec", {})
                if isinstance(spec, dict) and spec.get("type") == "NodePort":
                    total += 1

        return total