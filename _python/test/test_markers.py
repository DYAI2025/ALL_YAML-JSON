import pytest
from semantic_grabber import SemanticGrabber
from detectors.atomic_detector import AtomicDetector

# Lade die Marker-YAML
import yaml
markers = yaml.safe_load(open("self_protection_deception_markers.yaml", encoding="utf-8"))

grabber = SemanticGrabber(markers)
atomic = AtomicDetector(markers)

@pytest.mark.parametrize("text, expected_id", [
    ("Um ehrlich zu sein, es gab …", "A_PARTIAL_DISCLOSURE"),
    ("Ach, das ist doch nicht so schlimm.", "A_DOWNPLAYING"),
    ("Du übertreibst mal wieder 🙄", "A_GASLIGHT"),
])
def test_atomic_markers(text, expected_id):
    feats = grabber.extract(text)
    res = atomic.detect(text, feats)
    assert expected_id in res, f"{expected_id} nicht gefunden in {res}"
