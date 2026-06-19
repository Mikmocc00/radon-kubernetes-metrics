import numpy as np

from ..utils import ParsedManifest
from .field_entropy import FieldEntropy
from .manifest_complexity_ratio import ManifestComplexityRatio
from .misconfig_density import MisconfigDensity
from .scheduling_complexity import SchedulingComplexity
from .config_stress import ConfigStress


class KubernetesRiskIndex:

    WEIGHTS = {
        "field_entropy": 0.30,
        "manifest_complexity_ratio": 0.20,
        "misconfig_density": 0.20,
        "scheduling_complexity": 0.15,
        "config_stress": 0.15,
    }

    def __init__(self, manifests: list[ParsedManifest]):
        self.manifests = manifests

    @staticmethod
    def _zscore(values: np.ndarray) -> np.ndarray:
        std = values.std()
        if std == 0:
            return np.zeros_like(values)
        return (values - values.mean()) / std

    def count(self) -> list[float]:
        field_entropy = np.array(
            [FieldEntropy(m).count() for m in self.manifests]
        )
        manifest_complexity_ratio = np.array(
            [ManifestComplexityRatio(m).count() for m in self.manifests]
        )
        misconfig_density = np.array(
            [MisconfigDensity(m).count() for m in self.manifests]
        )
        scheduling_complexity = np.array(
            [SchedulingComplexity(m).count() for m in self.manifests]
        )
        config_stress = np.array(
            [ConfigStress(m).count() for m in self.manifests]
        )

        fe = self._zscore(field_entropy)
        mcr = self._zscore(manifest_complexity_ratio)
        md = self._zscore(misconfig_density)
        sc = self._zscore(scheduling_complexity)
        cs = self._zscore(config_stress)

        index = (
            self.WEIGHTS["field_entropy"] * fe
            + self.WEIGHTS["manifest_complexity_ratio"] * mcr
            + self.WEIGHTS["misconfig_density"] * md
            + self.WEIGHTS["scheduling_complexity"] * sc
            + self.WEIGHTS["config_stress"] * cs
        )

        return index.tolist()