from ..utils import ParsedManifest


class ResourceGovernanceRatio:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_resource_limits = 0
        num_resource_requests = 0
        num_containers = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            spec = doc.get("spec", {})
            if "template" in spec and isinstance(spec["template"], dict):
                pod_spec = spec["template"].get("spec", {})
            else:
                pod_spec = spec

            if not isinstance(pod_spec, dict):
                continue

            containers = pod_spec.get("containers", [])
            init_containers = pod_spec.get("initContainers", [])

            if not isinstance(containers, list):
                containers = []
            if not isinstance(init_containers, list):
                init_containers = []

            all_containers = containers + init_containers
            num_containers += len(all_containers)

            for c in all_containers:
                if not isinstance(c, dict):
                    continue

                resources = c.get("resources", {})
                if not isinstance(resources, dict):
                    continue

                if resources.get("limits"):
                    num_resource_limits += 1
                if resources.get("requests"):
                    num_resource_requests += 1

        numerator = num_resource_limits + num_resource_requests
        denominator = max(num_containers * 2, 1)

        return numerator / denominator