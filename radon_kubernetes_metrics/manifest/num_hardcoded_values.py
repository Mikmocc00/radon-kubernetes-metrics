from ..utils import ParsedManifest

class NumHardcodedValues:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            spec = doc.get("spec", {})
            if "template" in spec and isinstance(spec["template"], dict):
                spec = spec["template"].get("spec", {})

            containers = spec.get("containers", [])
            if isinstance(containers, list):
                for c in containers:
                    if isinstance(c, dict):
                        env_vars = c.get("env", [])
                        if isinstance(env_vars, list):
                            for env in env_vars:
                                if isinstance(env, dict) and "value" in env and "valueFrom" not in env:
                                    total += 1

        return total