import re
from ..utils import ParsedManifest


class DeploymentRiskScore:

    DEPRECATED_API_VERSIONS = {
        "extensions/v1beta1",
        "apps/v1beta1",
        "apps/v1beta2",
        "networking.k8s.io/v1beta1",
        "rbac.authorization.k8s.io/v1alpha1",
        "rbac.authorization.k8s.io/v1beta1",
        "storage.k8s.io/v1beta1",
        "apiextensions.k8s.io/v1beta1",
        "admissionregistration.k8s.io/v1beta1",
        "batch/v1beta1",
        "autoscaling/v2beta1",
        "autoscaling/v2beta2",
        "policy/v1beta1",
    }

    _HARDCODED_PATTERNS = [
        re.compile(r'(?i)(password|passwd|secret|token|api_key|apikey)\s*[:=]\s*\S+'),
        re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
        re.compile(r'(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*'),   
    ]

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest


    def _is_hardcoded(self, value: str) -> bool:
        for pattern in self._HARDCODED_PATTERNS:
            if pattern.search(value):
                return True
        return False

    def _count_hardcoded_in_env(self, containers: list) -> int:
        total = 0
        for c in containers:
            if not isinstance(c, dict):
                continue
            for env in c.get("env", []) or []:
                if not isinstance(env, dict):
                    continue
                if "value" in env and "valueFrom" not in env:
                    val = str(env.get("value", ""))
                    if self._is_hardcoded(f"{env.get('name', '')}={val}"):
                        total += 1
        return total


    def count(self):
        num_latest_tag = 0
        num_image_pull_policy_always = 0
        num_hardcoded_values = 0
        num_deprecated_api_versions = 0
        num_resources = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            num_resources += 1

            api_version = doc.get("apiVersion", "")
            if isinstance(api_version, str) and api_version in self.DEPRECATED_API_VERSIONS:
                num_deprecated_api_versions += 1

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

            for c in all_containers:
                if not isinstance(c, dict):
                    continue

                image = c.get("image", "")
                if isinstance(image, str):
                    tag = image.split(":")[-1] if ":" in image else "latest"
                    if tag == "latest":
                        num_latest_tag += 1

                pull_policy = c.get("imagePullPolicy", "")
                if isinstance(pull_policy, str) and pull_policy == "Always":
                    num_image_pull_policy_always += 1

            num_hardcoded_values += self._count_hardcoded_in_env(all_containers)

        numerator = (
            num_latest_tag
            + num_image_pull_policy_always
            + num_hardcoded_values
            + num_deprecated_api_versions
        )
        denominator = max(num_resources, 1)

        return numerator / denominator