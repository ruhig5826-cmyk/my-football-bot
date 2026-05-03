from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import asyncio
import config
from processing.filter import is_relevant
from processing.translator import translate_text
from processing.image_handler import get_image
from publisher.queue_manager import enqueue_post
from collector.deduplicator import is_duplicate, mark_seen

client = TelegramClient("session", config.API_ID, config.API_HASH)

@client.on(events.NewMessage(chats=config.SOURCE_CHANNELS))
async def handle_new_message(event):
    msg = event.message
    text = msg.message or ""

    if not text or len(text.strip()) < 20:
        return

    if is_duplicate(text):
        return

    if not is_relevant(text):
        return

    mark_seen(text)
    translated = await translate_text(text)
    image_path = await get_image(msg, text)
    await enqueue_post(translated, image_path, source=event.chat.username or str(event.chat_id))

async def start_listener():
    await client.start(bot_token=config.BOT_TOKEN)
    print("✅ Telegram listener started")
    await client.run_until_disconnected()
