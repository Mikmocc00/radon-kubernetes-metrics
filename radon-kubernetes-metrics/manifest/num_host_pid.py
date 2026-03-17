import yaml


class NumHostPID:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            spec = doc.get("spec", {})
            if spec.get("hostPID") is True:
                total += 1

        return total