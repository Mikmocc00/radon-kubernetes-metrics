import yaml


class AvgContainersPerPod:

    def __init__(self, script):
        self.script = script

    def count(self):
        docs = yaml.safe_load_all(self.script)

        total_containers = 0
        pod_count = 0

        for doc in docs:
            if not doc:
                continue

            spec = doc.get("spec", {})

            # Caso workload (Deployment, Job, ecc.)
            if "template" in spec:
                spec = spec["template"].get("spec", {})
                pod_count += 1

            # Caso Pod diretto
            elif "containers" in spec:
                pod_count += 1

            containers = spec.get("containers", [])
            total_containers += len(containers)

        if pod_count == 0:
            return 0

        return total_containers / pod_count