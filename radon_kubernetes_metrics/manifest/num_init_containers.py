import yaml


class NumInitContainers:

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

            init_containers = spec.get("initContainers", [])
            total += len(init_containers)

        return total