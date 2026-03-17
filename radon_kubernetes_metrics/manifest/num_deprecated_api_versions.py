import yaml


class NumDeprecatedAPIVersions:

    # Lista estendibile (puoi aggiornarla in base alla versione K8s target)
    DEPRECATED_PATTERNS = [
        "v1beta1",
        "v1alpha1",
        "extensions/",
    ]

    def __init__(self, script):
        self.script = script

    def count(self):

        docs = yaml.safe_load_all(self.script)
        total = 0

        for doc in docs:
            if not doc:
                continue

            api_version = doc.get("apiVersion", "")

            if any(pattern in api_version for pattern in self.DEPRECATED_PATTERNS):
                total += 1

        return total