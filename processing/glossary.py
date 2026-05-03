import json
from pathlib import Path

GLOSSARY_PATH = Path(__file__).resolve().parent.parent / "data" / "glossary.json"

FOOTBALL_GLOSSARY = {}

try:
    with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
        FOOTBALL_GLOSSARY = json.load(f)
except FileNotFoundError:
    FOOTBALL_GLOSSARY = {}
