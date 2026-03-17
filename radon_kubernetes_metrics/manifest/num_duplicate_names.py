import yaml


class NumDuplicateNames:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = list(yaml.safe_load_all(self.script))
        names = []

        for doc in docs:
            if not doc:
                continue

            name = doc.get("metadata", {}).get("name")
            if name:
                names.append(name)

        return len(names) - len(set(names))