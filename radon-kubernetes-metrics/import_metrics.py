# ---------------- GENERAL ----------------

from general.lines_code import LinesCode
from general.lines_blank import LinesBlank
from general.lines_comment import LinesComment

from general.num_suspicious_comments import NumSuspiciousComments
from general.num_tokens import NumTokens
from general.text_entropy import TextEntropy


# ---------------- MANIFEST (KUBERNETES) ----------------

from manifest.num_resources import NumResources
from manifest.num_kinds import NumKinds
from manifest.num_total_fields import NumTotalFields
from manifest.avg_fields_per_resource import AvgFieldsPerResource
from manifest.manifest_structural_complexity import ManifestStructuralComplexity
from manifest.config_entropy import ConfigEntropy
from manifest.nested_object_ratio import NestedObjectRatio


from manifest.num_containers import NumContainers
from manifest.num_init_containers import NumInitContainers
from manifest.avg_containers_per_pod import AvgContainersPerPod

from manifest.num_images import NumImages
from manifest.num_latest_tag import NumLatestTag
from manifest.num_image_pull_policy_always import NumImagePullPolicyAlways

from manifest.num_resource_limits import NumResourceLimits
from manifest.num_resource_requests import NumResourceRequests
from manifest.num_missing_resources import NumMissingResources

from manifest.num_privileged_containers import NumPrivilegedContainers
from manifest.num_run_as_root import NumRunAsRoot
from manifest.num_capabilities_added import NumCapabilitiesAdded
from manifest.num_host_network import NumHostNetwork
from manifest.num_host_pid import NumHostPID
from manifest.num_host_ipc import NumHostIPC
from manifest.num_secrets_usage import NumSecretsUsage

from manifest.num_services import NumServices
from manifest.num_ingresses import NumIngresses
from manifest.num_ports import NumPorts
from manifest.num_node_ports import NumNodePorts

from manifest.num_config_maps import NumConfigMaps
from manifest.num_volumes import NumVolumes
from manifest.num_persistent_volumes import NumPersistentVolumes

from manifest.num_liveness_probes import NumLivenessProbes
from manifest.num_readiness_probes import NumReadinessProbes
from manifest.num_startup_probes import NumStartupProbes
from manifest.num_missing_probes import NumMissingProbes

from manifest.num_hardcoded_values import NumHardcodedValues
from manifest.num_duplicate_names import NumDuplicateNames
from manifest.num_labels import NumLabels
from manifest.num_annotations import NumAnnotations

from manifest.num_deprecated_api_versions import NumDeprecatedAPIVersions

from manifest.num_affinity_rules import NumAffinityRules
from manifest.num_tolerations import NumTolerations
from manifest.num_node_selectors import NumNodeSelectors
# ---------------- KUBERNETES METRICS ----------------

# ---------------- GENERAL ----------------

general_metrics = {
    'lines_code': LinesCode,
    'lines_blank': LinesBlank,
    'lines_comment': LinesComment,
    'num_suspicious_comments': NumSuspiciousComments,
    'num_tokens': NumTokens,
    'text_entropy': TextEntropy
}

kubernetes_metrics = {

    # structure
    'num_resources': NumResources,
    'num_kinds': NumKinds,

    # containers
    'num_containers': NumContainers,
    'num_init_containers': NumInitContainers,
    'avg_containers_per_pod': AvgContainersPerPod,

    # images
    'num_images': NumImages,
    'num_latest_tag': NumLatestTag,
    'num_image_pull_policy_always': NumImagePullPolicyAlways,

    # resources
    'num_resource_limits': NumResourceLimits,
    'num_resource_requests': NumResourceRequests,
    'num_missing_resources': NumMissingResources,

    # security
    'num_privileged_containers': NumPrivilegedContainers,
    'num_run_as_root': NumRunAsRoot,
    'num_capabilities_added': NumCapabilitiesAdded,
    'num_host_network': NumHostNetwork,
    'num_host_pid': NumHostPID,
    'num_host_ipc': NumHostIPC,
    'num_secrets_usage': NumSecretsUsage,

    # networking
    'num_services': NumServices,
    'num_ingresses': NumIngresses,
    'num_ports': NumPorts,
    'num_nodeports': NumNodePorts,

    # config & storage
    'num_configmaps': NumConfigMaps,
    'num_volumes': NumVolumes,
    'num_persistent_volumes': NumPersistentVolumes,

    # reliability
    'num_liveness_probes': NumLivenessProbes,
    'num_readiness_probes': NumReadinessProbes,
    'num_startup_probes': NumStartupProbes,
    'num_missing_probes': NumMissingProbes,

    # smells
    'num_hardcoded_values': NumHardcodedValues,
    'num_duplicate_names': NumDuplicateNames,
    'num_labels': NumLabels,
    'num_annotations': NumAnnotations,

    # versioning
    'num_deprecated_api_versions': NumDeprecatedAPIVersions,

    # scheduling
    'num_affinity_rules': NumAffinityRules,
    'num_tolerations': NumTolerations,
    'num_node_selectors': NumNodeSelectors,

    'num_total_fields': NumTotalFields,
    'avg_fields_per_resource': AvgFieldsPerResource,
    'manifest_structural_complexity': ManifestStructuralComplexity,
    'config_entropy': ConfigEntropy,
    'nested_object_ratio': NestedObjectRatio,
}