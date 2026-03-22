from ..utils import ParsedManifest

class NumPrivilegedContainers:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            spec = doc.get("spec", {})
            if "template" in spec and isinstance(spec["template"], dict):
                spec = spec["template"].get("spec", {})

            containers = spec.get("containers", [])
            init_containers = spec.get("initContainers", [])

            if not isinstance(containers, list): containers = []
            if not isinstance(init_containers, list): init_containers = []

            for c in containers + init_containers:
                if isinstance(c, dict):
                    sc = c.get("securityContext", {})
                    if isinstance(sc, dict) and sc.get("privileged") is True:
                        total += 1

        return total