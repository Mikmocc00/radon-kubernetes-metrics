import yaml


class NumAnnotations:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            annotations = doc.get("metadata", {}).get("annotations", {})
            total += len(annotations)

        return total