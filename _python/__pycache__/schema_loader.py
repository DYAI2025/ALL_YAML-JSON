import json

class SchemaLoader:
    def __init__(self, schema_path):
        self.schema_path = schema_path
        self.schema = self.load_schema()

    def load_schema(self):
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_included_marker_names(self):
        markers = []
        for group in ["atomic_markers", "cluster_markers", "semantic_markers", "meta_markers"]:
            entries = self.schema.get("marker_detection", {}).get(group, [])
            markers.extend([entry["name"] for entry in entries])
        return markers

    def get_drift_axes(self):
        return self.schema.get("drift_analysis", {}).get("drift_axes", [])

    def get_metrics(self):
        return self.schema.get("relationship_inference", {})

    def get_visualization_options(self):
        return self.schema.get("outputs", {}).get("visualization", [])

    def get_export_formats(self):
        return self.schema.get("outputs", {}).get("export_format", [])


# Beispielhafte Nutzung:
# loader = SchemaLoader("schemas/beziehungsanalyse_schema.json")
# print(loader.get_included_marker_names())
# print(loader.get_drift_axes())
# print(loader.get_metrics())
