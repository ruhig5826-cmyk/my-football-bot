from datetime import datetime

EMOJI_MAP = {
    "goal": "⚽",
    "transfer": "🔄",
    "injury": "🏥",
    "red card": "🟥",
    "yellow card": "🟨",
    "win": "🏆",
    "loss": "❌",
    "draw": "🤝",
    "breaking": "🚨",
    "official": "✅",
    "deadline": "⏰",
    "loan": "📋"
}


def detect_emoji(text: str) -> str:
    text_lower = text.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in text_lower:
            return emoji
    return "⚽"


def format_post(translated_text: str, source: str) -> str:
    emoji = detect_emoji(translated_text)
    timestamp = datetime.now().strftime("%H:%M")
    source_label = f"@{source}" if source and not source.startswith("@") else source
    source_label = source_label or "Unknown"

    return f"{emoji} {translated_text}\n\n━━━━━━━━━━━━━━\n📡 ምንጭ: {source_label}\n🕐 {timestamp} | #축 soccer #ኢትዮጵያ #EthiopianFootball\n⚽ @YourChannelName"
