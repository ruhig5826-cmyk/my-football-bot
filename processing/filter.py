import re

RELEVANT_KEYWORDS = [
    "goal", "transfer", "injury", "match", "score", "win", "loss",
    "draw", "loan", "contract", "official", "squad", "fixture",
    "premier league", "league", "cup", "champions league",
    "penalty", "red card", "yellow card", "manager"
]


def is_relevant(text: str) -> bool:
    normalized = text.lower()
    score = sum(1 for keyword in RELEVANT_KEYWORDS if keyword in normalized)
    if score >= 1:
        return True
    if re.search(r"\b(EPL|UCL|Euro|WC|World Cup|CAF)\b", text, re.IGNORECASE):
        return True
    return False
