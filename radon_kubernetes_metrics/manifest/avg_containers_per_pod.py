from ..utils import ParsedManifest

class AvgContainersPerPod:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total_containers = 0
        pod_count = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            spec = doc.get("spec", {})

            if "template" in spec and isinstance(spec["template"], dict):
                spec = spec["template"].get("spec", {})
                pod_count += 1

            elif "containers" in spec:
                pod_count += 1

            containers = spec.get("containers", [])
            if isinstance(containers, list):
                total_containers += len(containers)

        if pod_count == 0:
            return 0

        return total_containers / pod_count