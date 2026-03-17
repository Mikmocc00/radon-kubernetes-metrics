import yaml
from ..utils import all_keys


class AvgFieldsPerResource:

    def __init__(self, script):
        self.script = script

    def count(self):

        docs = list(yaml.safe_load_all(self.script))

        if not docs:
            return 0

        total_fields = 0
        resource_count = 0

        for doc in docs:
            if not doc:
                continue

            total_fields += len(all_keys(doc))
            resource_count += 1

        if resource_count == 0:
            return 0

        return total_fields / resource_count