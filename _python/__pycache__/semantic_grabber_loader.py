
import yaml
from typing import List, Dict

class SemanticGrabberLibrary:
    def __init__(self, yaml_path: str):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            self.library = yaml.safe_load(f)

    def get_grabber_ids(self) -> List[str]:
        return list(self.library.keys())

    def get_patterns_for_id(self, grabber_id: str) -> List[str]:
        return self.library.get(grabber_id, {}).get('patterns', [])

    def get_description_for_id(self, grabber_id: str) -> str:
        return self.library.get(grabber_id, {}).get('beschreibung', '')

    def match_text(self, text: str, threshold: float = 0.6) -> List[str]:
        """ Dummy logic – to be replaced with semantic similarity models """
        matches = []
        for grabber_id, data in self.library.items():
            for pattern in data.get('patterns', []):
                if pattern.lower() in text.lower():
                    matches.append(grabber_id)
                    break
        return matches
