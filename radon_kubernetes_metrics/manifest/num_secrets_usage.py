import yaml


class NumSecretsUsage:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            spec = doc.get("spec", {})
            if "template" in spec:
                spec = spec["template"].get("spec", {})

            # envFrom
            containers = spec.get("containers", [])
            for c in containers:
                for env_from in c.get("envFrom", []):
                    if "secretRef" in env_from:
                        total += 1

                # env
                for env in c.get("env", []):
                    if "valueFrom" in env and "secretKeyRef" in env["valueFrom"]:
                        total += 1

        return total