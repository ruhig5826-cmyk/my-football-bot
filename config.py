import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "")
UNSPLASH_KEY = os.getenv("UNSPLASH_KEY", "")

SOURCE_CHANNELS = [
    "FabrizioRomano",
    "footballinsider247",
    "bisrat_sport_433et",
    "Sport_433et",
    "tikvahethsport",
    "dailysportethiopia",
    "soccer_ethiopia",
    "ethiopianlea",
    "Obnsports",
    "EthiopiaWFL",
    "Dirreeispoorti",
    "allfootballss",
    "transfer_news_football",
    "deadlinedaylive_en",
    "FootyNews",
    "Sky_Sports_Football",
]

MAX_POSTS_PER_HOUR = 20
TRANSLATION_LANGUAGE = "am"
