from ..utils import ParsedManifest

class NumDeprecatedAPIVersions:

    DEPRECATED_PATTERNS = [
        "v1beta1",
        "v1alpha1",
        "extensions/",
    ]

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest

    def count(self):
        total = 0

        for doc in self.manifest.docs:
            if not isinstance(doc, dict):
                continue

            api_version = doc.get("apiVersion", "")

            if isinstance(api_version, str):
                if any(pattern in api_version for pattern in self.DEPRECATED_PATTERNS):
                    total += 1

        return total