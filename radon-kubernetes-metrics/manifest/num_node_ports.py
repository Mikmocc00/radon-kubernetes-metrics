import yaml


class NumNodePorts:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            if doc.get("kind") == "Service":
                spec = doc.get("spec", {})
                if spec.get("type") == "NodePort":
                    total += 1

        return total