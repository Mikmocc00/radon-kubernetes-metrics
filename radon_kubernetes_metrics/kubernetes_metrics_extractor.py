from import_metrics import general_metrics, manifest_metrics
from .utils import ParsedManifest

def extract_kubernetes(script: str):

    if script is None:
        raise TypeError('Expected a string')

    results = dict()

    for name in general_metrics:
        try:
            results[name] = general_metrics[name](script).count()
        except Exception:
            results[name] = 0

    try:
        manifest = ParsedManifest(script)
    except Exception:
        return results

    for name in manifest_metrics:
        try:
            results[name] = manifest_metrics[name](manifest).count()
        except Exception:
            results[name] = 0

    return results