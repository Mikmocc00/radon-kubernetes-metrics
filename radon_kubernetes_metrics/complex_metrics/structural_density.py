from ..utils import ParsedManifest


class StructuralDensity:

    def __init__(self, manifest: ParsedManifest):
        self.manifest = manifest


    @staticmethod
    def _count_nested_objects(node, depth: int = 0) -> tuple[int, int]:
        total_fields = 0
        nested_objects = 0

        if isinstance(node, dict):
            for v in node.values():
                total_fields += 1
                if isinstance(v, dict) and depth >= 0:
                    nested_objects += 1
                    sub_fields, sub_nested = StructuralDensity._count_nested_objects(v, depth + 1)
                    total_fields += sub_fields
                    nested_objects += sub_nested
                elif isinstance(v, list):
                    sub_fields, sub_nested = StructuralDensity._count_nested_objects(v, depth)
                    total_fields += sub_fields
                    nested_objects += sub_nested
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, (dict, list)):
                    sub_fields, sub_nested = StructuralDensity._count_nested_objects(item, depth)
                    total_fields += sub_fields
                    nested_objects += sub_nested

        return total_fields, nested_objects


    def count(self):
        num_resources = 0
        total_fields_all = 0
        nested_objects_all = 0

        for doc in self.manifest.docs:
            if not doc:
                continue

            num_resources += 1
            fields, nested = self._count_nested_objects(doc)
            total_fields_all += fields
            nested_objects_all += nested

        manifest_structural_complexity = total_fields_all * num_resources

        nested_object_ratio = nested_objects_all / max(total_fields_all, 1)

        numerator = manifest_structural_complexity * nested_object_ratio
        denominator = max(num_resources, 1)

        return numerator / denominator