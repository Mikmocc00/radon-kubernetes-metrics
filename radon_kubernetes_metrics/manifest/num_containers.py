import yaml

class NumContainers:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            # Pod-like resources
            spec = doc.get("spec", {})

            # Template-based resources (Deployment, etc.)
            if "template" in spec:
                spec = spec["template"].get("spec", {})

            containers = spec.get("containers", [])
            total += len(containers)

        return total