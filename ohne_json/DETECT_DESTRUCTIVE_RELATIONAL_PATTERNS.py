# coding: utf-8
from typing import List, Dict
from base_marker_detector import BaseMarkerDetector  # abstract base
from marker_matcher import MarkerMatcher  # engine for marker access
from scoring_utils import score_risk_level  # utility for scoring risk

class DETECT_DESTRUCTIVE_RELATIONAL_PATTERNS(BaseMarkerDetector):
    """
    Rekursiver Meta-Detector für destruktive Beziehungsmuster.
    Erkennt kumulative Aktivierung typischer Schutz- und Destabilisierungsstrategien
    wie Schuldumkehr, Bindungsambivalenz, emotionale Instabilität etc.
    """

    ID = "MM_DESTRUCTIVE_RELATIONAL_PATTERNS"
    LEVEL = 4
    VERSION = "1.0.0"
    LANG = "de"
    PRIORITY = "high"
    WEIGHT = 2.3
    TAGS = ["schutzmuster", "bindung", "destabilisierung", "emotion_drift"]

    REQUIRED_MARKERS = [
        "C_DESTRUCTIVE_SELF_PROTECTION",
        "C_RELATIONAL_DESTABILIZATION_LOOP",
        "C_EMO_INSTABILITY",
        "C_ADAPTIVE_POLARIZATION",
        "C_SVT_MESSAGE_INCONGRUENCE"
    ]

    TRIGGER_THRESHOLD = 3  # mindestens drei Cluster aktiv

    def detect(self, chunk: Dict, matcher: MarkerMatcher) -> Dict:
        """
        Analysefunktion zur Bewertung eines Chunks.
        Gibt ein dict mit Treffer, Score und Trigger-Markern zurück.
        """
        triggered = []
        for marker_id in self.REQUIRED_MARKERS:
            if matcher.is_active(marker_id, chunk):
                triggered.append(marker_id)

        result = {
            "marker_id": self.ID,
            "score": 0,
            "matched": False,
            "triggered_markers": triggered,
            "details": {}
        }

        if len(triggered) >= self.TRIGGER_THRESHOLD:
            result["matched"] = True
            result["score"] = score_risk_level(len(triggered), self.TRIGGER_THRESHOLD, self.WEIGHT)
            result["details"]["message"] = f"{len(triggered)} destruktive Cluster aktiv (von {self.TRIGGER_THRESHOLD} benötigt)"
        else:
            result["details"]["message"] = f"{len(triggered)} Cluster erkannt, Schwelle nicht erreicht"

        return result
