from import_metrics import general_metrics, kubernetes_metrics


def extract_kubernetes(script: str):

    if script is None:
        raise TypeError('Expected a string')

    metrics = general_metrics
    metrics.update(kubernetes_metrics)

    results = dict()

    for name in metrics:
        results[name] = metrics[name](script).count()

    return results