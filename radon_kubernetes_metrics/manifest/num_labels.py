import yaml


class NumLabels:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            labels = doc.get("metadata", {}).get("labels", {})
            total += len(labels)

        return total