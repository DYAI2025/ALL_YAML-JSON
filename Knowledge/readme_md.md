# Marker Analysis Engine

Ein hochmodernes Analyse- und Visualisierungstool für Beziehungschroniken, spezialisiert auf die Erkennung von Kommunikationsmustern, Marker-Treffern und potentiellen Fraud-Szenarien.

## 🎯 Zielsetzung

Das System erkennt und analysiert automatisch psychosoziale Marker in Dialogen und Chat-Transkripten:
- **Fraud-Indikatoren**: Romance Scam, Love Bombing, Financial Manipulation
- **Beziehungsmuster**: Gaslighting, Blame-Shift, Manipulation, Territorialität
- **Positive Marker**: Wertschätzung, Empathie, Resilienz, konstruktive Kommunikation

## 🚀 Features

- **Dynamisches Marker-Loading**: YAML/TXT/JSON Marker-Definitionen werden zur Laufzeit geladen
- **Intelligentes Text-Chunking**: Automatische Segmentierung nach Zeit, Sprecher und Kontext
- **Fuzzy-Matching**: Erkennung von Marker-Varianten und semantisch ähnlichen Mustern
- **Scoring-Engine**: Berechnung von Beziehungsgesundheit, Manipulationsgrad etc. (1-10 Skala)
- **Zeitreihen-Analyse**: Entwicklung von Mustern über Zeit visualisierbar
- **Sprecher-Attribution**: Individuelle Analyse pro Gesprächsteilnehmer

## 📋 Requirements

- Python 3.9+
- Siehe `requirements.txt` für alle Dependencies

## 🛠️ Installation

```bash
# Repository klonen
git clone <repository-url>
cd marker_scripts

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# Development-Installation
pip install -e .
```

## 🎮 Quick Start

```python
from src.chunker import TextChunker
from src.matcher import MarkerMatcher
from src.scoring import ScoringEngine

# Text in Chunks aufteilen
chunker = TextChunker()
chunks = chunker.process_text(chat_text)

# Marker laden und matchen
matcher = MarkerMatcher()
matcher.load_markers("markers/romance_scam_markers.yaml")
matches = matcher.find_matches(chunks)

# Scoring durchführen
scorer = ScoringEngine()
scores = scorer.calculate_scores(matches)
```

## 📚 Dokumentation

- [API Dokumentation](docs/API.md)
- [Marker Definition Guide](docs/MARKERS_GUIDE.md)
- [Verwendungsbeispiele](docs/USAGE.md)

## 🧪 Testing

```bash
# Alle Tests ausführen
pytest

# Mit Coverage-Report
pytest --cov=src --cov-report=html

# Nur spezifische Tests
pytest tests/test_matcher/
```

## 📊 Beispiel-Output

```json
{
  "chunks": [
    {
      "id": "chunk_001",
      "speaker": "Person A",
      "timestamp": "2024-01-15 14:30:00",
      "markers_found": ["love_bombing", "future_faking"],
      "score": 8.5
    }
  ],
  "overall_scores": {
    "manipulation_index": 7.2,
    "relationship_health": 3.1,
    "fraud_probability": 0.78
  }
}
```

## 🤝 Contributing

1. Fork das Repository
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Changes committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.