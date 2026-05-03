# my-football-bot

## 🏗️ Project Blueprint

This repository contains a complete professional architecture for an Amharic-focused Telegram football bot. The system listens to football news sources, filters relevance, translates English updates to Amharic, enriches posts with images, and publishes them to your Telegram channel.

## 📁 Project Structure

```
football_bot/
├── main.py                 # Entry point
├── collector/
│   ├── telegram_listener.py   # Reads source channels via Telethon
│   ├── rss_poller.py          # RSS + football-data.org polling
│   └── deduplicator.py        # Hash-based duplication guard
├── processing/
│   ├── filter.py              # Relevance scoring
│   ├── translator.py          # EN→AM translation engine
│   ├── glossary.py            # Loads football glossary
│   └── image_handler.py       # Fetch/generate/watermark images
├── publisher/
│   ├── formatter.py           # Format Amharic caption with emojis
│   ├── queue_manager.py       # SQLite queue + dedup support
│   └── bot_publisher.py       # Sends posts to your Telegram channel
├── data/
│   ├── glossary.json          # English→Amharic glossary
│   └── bot.db                 # SQLite database (created at runtime)
├── config.py                 # Environment-driven configuration
├── requirements.txt          # Python dependencies
├── railway.json              # Railway hosting config
└── .gitignore
```

## ⚙️ How it Works

1. `main.py` starts the app and scheduler.
2. `collector/telegram_listener.py` listens to configured channels via Telethon.
3. `collector/rss_poller.py` polls RSS sources periodically.
4. `collector/deduplicator.py` prevents duplicates using SHA-256 hashes.
5. `processing/filter.py` rejects non-football or low-value content.
6. `processing/translator.py` translates English text to Amharic using Argos Translate.
7. `processing/image_handler.py` attaches images from message media or Unsplash.
8. `publisher/queue_manager.py` stores queued posts in SQLite.
9. `publisher/bot_publisher.py` publishes posts to your channel on a schedule.

## 🔧 Configuration

Create environment variables for your deployment:

- `BOT_TOKEN` — Telegram bot token from @BotFather
- `API_ID` — Telegram API ID from my.telegram.org
- `API_HASH` — Telegram API hash from my.telegram.org
- `CHANNEL_ID` — target Telegram channel username or ID
- `UNSPLASH_KEY` — Unsplash API key (optional)
- `FOOTBALL_API_KEY` — football-data.org API key (optional)

## ▶️ Run Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Export env vars or create a `.env` file.
3. Start the bot:
```bash
python main.py
```

## 🧠 Notes

- The glossary in `data/glossary.json` is a strong leverage point for translation quality.
- `railway.json` is included for Railway deployment; adjust if you deploy elsewhere.
- The bot architecture is intentionally modular so you can extend sources, filters, or translation logic.
