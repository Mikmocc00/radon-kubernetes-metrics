from ..utils import ParsedManifest


class NetworkExposureDensity:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_ports = 0
        num_node_ports = 0
        num_ingresses = 0
        num_services = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            kind = doc.get("kind", "")

            if kind == "Ingress":
                num_ingresses += 1

            if kind == "Service":
                num_services += 1

                spec = doc.get("spec", {})
                if not isinstance(spec, dict):
                    continue

                ports = spec.get("ports", [])
                if not isinstance(ports, list):
                    continue

                for port_entry in ports:
                    if not isinstance(port_entry, dict):
                        continue

                    num_ports += 1

                    if "nodePort" in port_entry:
                        num_node_ports += 1

            if kind in ("Pod", "Deployment", "StatefulSet", "DaemonSet",
                        "ReplicaSet", "Job", "CronJob"):
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

                for c in containers + init_containers:
                    if not isinstance(c, dict):
                        continue
                    container_ports = c.get("ports", [])
                    if isinstance(container_ports, list):
                        num_ports += len(container_ports)

        numerator = num_ports + num_node_ports + num_ingresses
        denominator = max(num_services + 1, 1)

        return numerator / denominator