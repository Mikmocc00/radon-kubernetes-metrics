import yaml


class NumHardcodedValues:

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

            containers = spec.get("containers", [])

            for c in containers:
                for env in c.get("env", []):
                    if "value" in env and "valueFrom" not in env:
                        total += 1

        return total