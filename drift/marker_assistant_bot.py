#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FRAUSAR Marker Assistant Bot
============================
Intelligenter Assistent für die automatische Pflege und Erweiterung 
der Love Scammer Erkennungsmarker.

Features:
- Automatische Marker-Updates
- Neue Pattern-Erkennung
- Konsistenz-Checks
- Performance-Optimierung
- Web-Scraping für neue Scam-Trends
"""

import os
import re
import yaml
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('marker_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FRAUSAR_Assistant')

class MarkerAssistant:
    """
    Intelligenter Assistent für die FRAUSAR Marker-Pflege
    """
    
    def __init__(self, marker_directory: str = "Assist_TXT_marker_py:/ALL_NEWMARKER01"):
        """
        Initialisiert den Marker-Assistenten
        
        Args:
            marker_directory: Pfad zum Marker-Verzeichnis
        """
        self.marker_dir = Path(marker_directory)
        self.backup_dir = self.marker_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Status-Tracking
        self.last_update = None
        self.marker_stats = {}
        
        logger.info(f"FRAUSAR Marker Assistant initialisiert für: {self.marker_dir}")
    
    def create_backup(self, marker_file: str) -> str:
        """
        Erstellt Backup einer Marker-Datei vor Änderungen
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{marker_file}_{timestamp}.backup"
        backup_path = self.backup_dir / backup_name
        
        source_path = self.marker_dir / marker_file
        if source_path.exists():
            backup_path.write_text(source_path.read_text(encoding='utf-8'), encoding='utf-8')
            logger.info(f"Backup erstellt: {backup_name}")
            return str(backup_path)
        return ""
    
    def analyze_marker_structure(self, marker_file: str) -> Dict[str, Any]:
        """
        Analysiert die Struktur einer Marker-Datei
        """
        file_path = self.marker_dir / marker_file
        if not file_path.exists():
            return {}
        
        content = file_path.read_text(encoding='utf-8')
        
        analysis = {
            "file": marker_file,
            "size": len(content),
            "lines": len(content.splitlines()),
            "examples_count": content.count('- "'),
            "has_semantic_grab": "semantic_grab:" in content,
            "has_regex_patterns": "pattern:" in content,
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime),
            "marker_type": self._detect_marker_type(content)
        }
        
        return analysis
    
    def _detect_marker_type(self, content: str) -> str:
        """
        Erkennt den Typ eines Markers basierend auf dem Inhalt
        """
        content_lower = content.lower()
        
        if "love_bombing" in content_lower or "zuneigung" in content_lower:
            return "emotional_manipulation"
        elif "gaslighting" in content_lower or "realität" in content_lower:
            return "psychological_manipulation"
        elif "geld" in content_lower or "money" in content_lower:
            return "financial_fraud"
        elif "isolation" in content_lower or "isolier" in content_lower:
            return "social_manipulation"
        else:
            return "general"
    
    def update_marker_examples(self, marker_file: str, new_examples: List[str]) -> bool:
        """
        Fügt neue Beispiele zu einem Marker hinzu
        """
        try:
            # Backup erstellen
            self.create_backup(marker_file)
            
            file_path = self.marker_dir / marker_file
            content = file_path.read_text(encoding='utf-8')
            
            # Neue Beispiele hinzufügen
            beispiele_section = re.search(r'beispiele:\s*\n(.*?)(?=\n\w+:|$)', content, re.DOTALL)
            if beispiele_section:
                existing_examples = beispiele_section.group(1)
                
                # Duplikate vermeiden
                for example in new_examples:
                    if example not in existing_examples:
                        formatted_example = f'  - "{example}"\n'
                        content = content.replace(
                            beispiele_section.group(0),
                            beispiele_section.group(0) + formatted_example
                        )
            
            file_path.write_text(content, encoding='utf-8')
            logger.info(f"Marker {marker_file} mit {len(new_examples)} neuen Beispielen aktualisiert")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Update von {marker_file}: {e}")
            return False
    
    def optimize_regex_patterns(self, marker_file: str) -> bool:
        """
        Optimiert Regex-Patterns für bessere Performance
        """
        try:
            self.create_backup(marker_file)
            
            file_path = self.marker_dir / marker_file
            content = file_path.read_text(encoding='utf-8')
            
            # Finde alle Regex-Patterns
            patterns = re.findall(r'pattern:\s*r"([^"]+)"', content)
            
            optimized_count = 0
            for pattern in patterns:
                # Einfache Optimierungen
                optimized = self._optimize_single_pattern(pattern)
                if optimized != pattern:
                    content = content.replace(f'r"{pattern}"', f'r"{optimized}"')
                    optimized_count += 1
            
            if optimized_count > 0:
                file_path.write_text(content, encoding='utf-8')
                logger.info(f"{optimized_count} Patterns in {marker_file} optimiert")
            
            return True
            
        except Exception as e:
            logger.error(f"Fehler bei Pattern-Optimierung von {marker_file}: {e}")
            return False
    
    def _optimize_single_pattern(self, pattern: str) -> str:
        """
        Optimiert ein einzelnes Regex-Pattern
        """
        # Case-insensitive Flags hinzufügen wenn nötig
        if not pattern.startswith("(?i)") and any(c.isupper() for c in pattern):
            pattern = f"(?i){pattern}"
        
        # Unnötige Gruppen entfernen
        pattern = re.sub(r'\(([^|()]+)\)', r'\1', pattern)
        
        # Häufige Optimierungen
        optimizations = {
            r'\s+': r'\s+',  # Mehrfache Leerzeichen
            r'[aä]': r'[aä]',  # Deutsche Umlaute
            r'[oö]': r'[oö]',
            r'[uü]': r'[uü]',
        }
        
        for old, new in optimizations.items():
            pattern = pattern.replace(old, new)
        
        return pattern
    
    def scan_for_new_trends(self) -> List[Dict[str, Any]]:
        """
        Scannt das Internet nach neuen Scammer-Trends
        (Vereinfachte Version - in der Praxis würde man APIs verwenden)
        """
        trends = []
        
        # Beispiel-Trends (würde in der Realität von Web-Scraping kommen)
        potential_trends = [
            {
                "pattern": "krypto.*investition.*schnell.*reich",
                "category": "financial_fraud",
                "confidence": 0.85,
                "source": "fraud_forum_analysis"
            },
            {
                "pattern": "militär.*einsatz.*telefonieren.*unmöglich",
                "category": "romance_scam",
                "confidence": 0.92,
                "source": "dating_app_reports"
            },
            {
                "pattern": "paket.*zoll.*gebühren.*sofort.*zahlen",
                "category": "delivery_scam",
                "confidence": 0.78,
                "source": "consumer_reports"
            }
        ]
        
        for trend in potential_trends:
            if trend["confidence"] > 0.8:
                trends.append(trend)
        
        logger.info(f"{len(trends)} neue Trends mit hoher Konfidenz erkannt")
        return trends
    
    def generate_marker_suggestions(self, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generiert Vorschläge für neue Marker basierend auf erkannten Trends
        """
        suggestions = []
        
        for trend in trends:
            suggestion = {
                "marker_name": f"{trend['category'].upper()}_TREND_{int(time.time())}",
                "description": f"Automatisch erkannter Trend: {trend['pattern']}",
                "pattern": trend['pattern'],
                "confidence": trend['confidence'],
                "source": trend['source'],
                "suggested_examples": self._generate_examples_for_pattern(trend['pattern'])
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_examples_for_pattern(self, pattern: str) -> List[str]:
        """
        Generiert Beispiele basierend auf einem Pattern
        """
        # Vereinfachte Beispiel-Generierung
        if "krypto" in pattern.lower():
            return [
                "Investiere jetzt in Bitcoin und werde schnell reich!",
                "Crypto-Investment mit 500% Gewinn garantiert!",
                "Schnelle Krypto-Gewinne - nur heute verfügbar!"
            ]
        elif "militär" in pattern.lower():
            return [
                "Bin auf Militäreinsatz, kann nicht telefonieren",
                "Einsatz im Ausland, Kommunikation streng begrenzt",
                "Mission geheim, Kontakt nur über Chat möglich"
            ]
        elif "paket" in pattern.lower():
            return [
                "Ihr Paket ist beim Zoll, zahlen Sie sofort 50€",
                "Zollgebühren für Ihr Paket müssen heute bezahlt werden",
                "Paket wird zurückgeschickt ohne sofortige Zahlung"
            ]
        else:
            return []
    
    def run_daily_maintenance(self):
        """
        Führt tägliche Wartungsroutinen aus
        """
        logger.info("=== Starte tägliche Marker-Wartung ===")
        
        # 1. Analysiere alle Marker
        for marker_file in self.marker_dir.glob("*.txt"):
            if marker_file.name.endswith("_MARKER.txt"):
                analysis = self.analyze_marker_structure(marker_file.name)
                self.marker_stats[marker_file.name] = analysis
        
        # 2. Suche nach neuen Trends
        trends = self.scan_for_new_trends()
        
        # 3. Generiere Vorschläge
        suggestions = self.generate_marker_suggestions(trends)
        
        # 4. Speichere Report
        report = {
            "timestamp": datetime.now().isoformat(),
            "marker_stats": self.marker_stats,
            "trends_found": len(trends),
            "suggestions": suggestions
        }
        
        report_path = self.marker_dir / "daily_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Wartung abgeschlossen. Report gespeichert: {report_path}")
        return report
    
    def interactive_update_session(self):
        """
        Startet eine interaktive Session für Marker-Updates
        """
        print("\n=== FRAUSAR Marker Assistant - Interaktive Session ===")
        print("1. Neuen Marker erstellen")
        print("2. Bestehenden Marker erweitern")
        print("3. Patterns optimieren")
        print("4. Trend-Analyse ausführen")
        print("5. Daily Maintenance")
        print("0. Beenden")
        
        while True:
            choice = input("\nWähle eine Option (0-5): ").strip()
            
            if choice == "0":
                print("Auf Wiedersehen!")
                break
            elif choice == "1":
                self._create_new_marker_interactive()
            elif choice == "2":
                self._extend_marker_interactive()
            elif choice == "3":
                self._optimize_patterns_interactive()
            elif choice == "4":
                trends = self.scan_for_new_trends()
                suggestions = self.generate_marker_suggestions(trends)
                print(f"\n{len(suggestions)} neue Trend-basierte Marker-Vorschläge:")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion['marker_name']} (Confidence: {suggestion['confidence']:.2f})")
            elif choice == "5":
                self.run_daily_maintenance()
            else:
                print("Ungültige Auswahl!")
    
    def _create_new_marker_interactive(self):
        """Interaktive Erstellung eines neuen Markers"""
        print("\n--- Neuen Marker erstellen ---")
        marker_name = input("Marker-Name: ").strip()
        description = input("Beschreibung: ").strip()
        
        marker_content = f"""marker: {marker_name}
beschreibung: >
  {description}
beispiele:
  - "Beispiel wird hinzugefügt"
semantic_grab:
  description: "Automatisch generiert"
  patterns:
    - rule: "AUTO_PATTERN"
      pattern: r"(automatisch.*generiert)"
tags: [auto_generated, needs_review]
"""
        
        file_path = self.marker_dir / f"{marker_name}.txt"
        file_path.write_text(marker_content, encoding='utf-8')
        print(f"Marker erstellt: {file_path}")
    
    def _extend_marker_interactive(self):
        """Interaktive Erweiterung eines bestehenden Markers"""
        print("\n--- Marker erweitern ---")
        marker_files = list(self.marker_dir.glob("*_MARKER.txt"))
        
        for i, file_path in enumerate(marker_files, 1):
            print(f"{i}. {file_path.name}")
        
        try:
            choice = int(input("Wähle Marker-Datei: ")) - 1
            if 0 <= choice < len(marker_files):
                marker_file = marker_files[choice].name
                new_example = input("Neues Beispiel: ").strip()
                if new_example:
                    self.update_marker_examples(marker_file, [new_example])
            else:
                print("Ungültige Auswahl!")
        except ValueError:
            print("Bitte eine Zahl eingeben!")
    
    def _optimize_patterns_interactive(self):
        """Interaktive Pattern-Optimierung"""
        print("\n--- Patterns optimieren ---")
        marker_files = list(self.marker_dir.glob("*_MARKER.txt"))
        
        for file_path in marker_files:
            print(f"Optimiere {file_path.name}...")
            self.optimize_regex_patterns(file_path.name)
        
        print("Pattern-Optimierung abgeschlossen!")

def main():
    """
    Hauptfunktion - startet den Marker Assistant
    """
    assistant = MarkerAssistant()
    
    # Kommandozeilen-Argumente könnten hier verarbeitet werden
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--daily":
            assistant.run_daily_maintenance()
        elif sys.argv[1] == "--interactive":
            assistant.interactive_update_session()
        else:
            print("Verfügbare Optionen: --daily, --interactive")
    else:
        assistant.interactive_update_session()

if __name__ == "__main__":
    main() 