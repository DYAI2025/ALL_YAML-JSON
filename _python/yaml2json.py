#!/usr/bin/env python3
"""
yaml2json.py  ·  WordThread Marker Engine Helper
------------------------------------------------
Wandelt alle .yaml|.yml-Dateien eines Verzeichnisses (rekursiv) oder eine
einzelne Datei in gleichnamige .json-Dateien um.

⤷   python yaml2json.py  markers/          # ganze Mappe
⤷   python yaml2json.py  markers/A_WZ.yaml # einzelne Datei

Optionen:
    --out DIR        Zielordner (default: <eingabepfad>/json_out)
    --schema FILE    JSON-Schema zur Validierung (optional)
    --indent N       Einrückung im Output-JSON (default: 2)
"""

import argparse, json, sys
from pathlib import Path
from datetime import datetime

try:
    from ruamel.yaml import YAML
except ModuleNotFoundError:
    sys.exit("❌  ruamel.yaml fehlt:  pip install ruamel.yaml")

try:
    import jsonschema
except ModuleNotFoundError:
    jsonschema = None  # Validierung nur, wenn verfügbar

yaml = YAML(typ="safe")
yaml.preserve_quotes = True   # kein Verlust bei Strings

def load_yaml(path: Path):
    """Liest alle YAML-Dokumente (---) aus einer Datei."""
    with path.open("r", encoding="utf-8") as f:
        return list(yaml.load_all(f))

def validate(obj, schema):
    """Optional: JSON-Schema-Validierung."""
    if jsonschema is None:
        raise RuntimeError("jsonschema nicht installiert")
    jsonschema.validate(obj, schema)

def convert_file(path: Path, out_dir: Path, schema, indent: int):
    docs = load_yaml(path)
    # Datei kann mehrere YAML-Dokumente enthalten → Liste serialisieren
    out_data = docs[0] if len(docs) == 1 else docs
    if schema:
        validate(out_data, schema)
    out_path = out_dir / (path.stem + ".json")
    out_path.write_text(
        json.dumps(out_data, ensure_ascii=False, indent=indent),
        encoding="utf-8"
    )
    print(f"✔  {path.name}  →  {out_path.relative_to(out_dir.parent)}")

def walk_inputs(input_path: Path):
    return (
        [input_path] if input_path.is_file()
        else sorted(input_path.rglob("*.yml")) + sorted(input_path.rglob("*.yaml"))
    )

def main():
    ap = argparse.ArgumentParser(description="YAML → JSON Converter")
    ap.add_argument("src", type=Path, help="Datei oder Verzeichnis mit YAML")
    ap.add_argument("--out", type=Path, help="Zielordner")
    ap.add_argument("--schema", type=Path, help="JSON-Schema (optional)")
    ap.add_argument("--indent", type=int, default=2)
    args = ap.parse_args()

    if not args.src.exists():
        sys.exit("❌  Eingabepfad existiert nicht.")

    out_dir = args.out or args.src.parent / "json_out"
    out_dir.mkdir(parents=True, exist_ok=True)

    schema = None
    if args.schema:
        if jsonschema is None:
            sys.exit("❌  jsonschema-Paket nicht installiert.")
        schema = json.loads(args.schema.read_text(encoding="utf-8"))

    files = walk_inputs(args.src)
    if not files:
        sys.exit("⚠️  Keine YAML-Dateien gefunden.")

    print(f"🏁  Starte Konvertierung ({len(files)} Dateien)  –  {datetime.now():%H:%M:%S}")
    for f in files:
        try:
            convert_file(f, out_dir, schema, args.indent)
        except Exception as e:
            print(f"⚠️  Fehler in {f}: {e}")

    print(f"✅  Fertig. JSON-Dateien liegen in  {out_dir.resolve()}")

if __name__ == "__main__":
    main()
