import yaml


class NumPersistentVolumes:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            kind = doc.get("kind")
            if kind in ["PersistentVolume", "PersistentVolumeClaim"]:
                total += 1

        return total