import yaml
from .utils import all_keys


class ManifestStructuralComplexity:

    def __init__(self, script):
        self.script = script

    def count(self):

        docs = list(yaml.safe_load_all(self.script))

        total_fields = 0
        resource_count = 0

        for doc in docs:
            if not doc:
                continue

            total_fields += len(all_keys(doc))
            resource_count += 1

        return total_fields * resource_count