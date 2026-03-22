from ..utils import ParsedManifest

class NumSecretsUsage:

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
                    if not isinstance(c, dict):
                        continue

                    # envFrom
                    env_from = c.get("envFrom", [])
                    if isinstance(env_from, list):
                        for ef in env_from:
                            if isinstance(ef, dict) and "secretRef" in ef:
                                total += 1

                    # env
                    env_list = c.get("env", [])
                    if isinstance(env_list, list):
                        for env in env_list:
                            if isinstance(env, dict) and "valueFrom" in env:
                                value_from = env["valueFrom"]
                                if isinstance(value_from, dict) and "secretKeyRef" in value_from:
                                    total += 1

        return total