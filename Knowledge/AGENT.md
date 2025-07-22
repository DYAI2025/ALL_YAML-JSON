# Marker Analysis Engine - Agent Guide

## Build/Test/Lint Commands
- **Test all**: `pytest` or `python -m pytest`
- **Test single file**: `pytest tests/test_filename.py`
- **Test with coverage**: `pytest --cov=src --cov-report=html`
- **Lint**: `pylint src/` or `flake8 src/`
- **Format**: `black src/` and `isort src/`
- **Type check**: `mypy src/`
- **Install dev deps**: `pip install -e .[dev]`

## Architecture
- **Core Engine**: Semantic marker detection system for analyzing relationship communication patterns and fraud detection
- **Main modules**: `_python/` contains core Python implementation with matcher, scoring, chunking, and aggregation engines
- **Marker definitions**: Root-level `.yaml` and `.txt` files define behavioral patterns (love scam, manipulation, gaslighting markers)
- **Data flow**: Text chunks → marker matching → scoring → time series aggregation → behavioral analysis

## Code Style
- **Format**: Black (88 char line length), isort for imports
- **Types**: Full type hints required (`disallow_untyped_defs = true`)
- **Imports**: Absolute imports from `src.`, relative for same module
- **Naming**: Snake_case for variables/functions, PascalCase for classes, CAPS for constants
- **Error handling**: Use custom exceptions, log with structured logging
- **Models**: Pydantic BaseModel for all data structures with validators
