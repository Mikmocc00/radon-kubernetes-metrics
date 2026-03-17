import yaml


class NestedObjectRatio:

    def __init__(self, script):
        self.script = script

    def count(self):

        docs = yaml.safe_load_all(self.script)

        total_fields = 0
        nested_fields = 0

        for doc in docs:
            if not doc:
                continue

            stack = [doc]

            while stack:
                current = stack.pop()

                if isinstance(current, dict):
                    for v in current.values():
                        total_fields += 1

                        if isinstance(v, dict) or isinstance(v, list):
                            nested_fields += 1
                            stack.append(v)

                elif isinstance(current, list):
                    for item in current:
                        if isinstance(item, dict) or isinstance(item, list):
                            nested_fields += 1
                            stack.append(item)

        if total_fields == 0:
            return 0

        return nested_fields / total_fields