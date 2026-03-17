import yaml


class NumMissingResources:

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

            containers = spec.get("containers", [])
            init_containers = spec.get("initContainers", [])

            for c in containers + init_containers:
                resources = c.get("resources", {})

                has_limits = "limits" in resources
                has_requests = "requests" in resources

                if not has_limits and not has_requests:
                    total += 1

        return total