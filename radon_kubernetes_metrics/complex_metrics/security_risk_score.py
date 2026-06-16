from ..utils import ParsedManifest


class SecurityRiskScore:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        num_privileged = 0
        num_run_as_root = 0
        num_capabilities_added = 0
        num_host_network = 0
        num_host_pid = 0
        num_host_ipc = 0
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

            if pod_spec.get("hostNetwork") is True:
                num_host_network += 1
            if pod_spec.get("hostPID") is True:
                num_host_pid += 1
            if pod_spec.get("hostIPC") is True:
                num_host_ipc += 1

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

                sc = c.get("securityContext", {})
                if not isinstance(sc, dict):
                    sc = {}

                if sc.get("privileged") is True:
                    num_privileged += 1

                run_as_root = sc.get("runAsNonRoot")
                run_as_user = sc.get("runAsUser")
                if run_as_root is False or run_as_user == 0:
                    num_run_as_root += 1

                caps = sc.get("capabilities", {})
                if isinstance(caps, dict):
                    added = caps.get("add", [])
                    if isinstance(added, list):
                        num_capabilities_added += len(added)

        numerator = (
            num_privileged
            + num_run_as_root
            + num_capabilities_added
            + num_host_network
            + num_host_pid
            + num_host_ipc
        )
        denominator = max(num_containers, 1)

        return numerator / denominator