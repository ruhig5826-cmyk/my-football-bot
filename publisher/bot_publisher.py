import os
from telegram import Bot
from telegram.constants import ParseMode
from publisher.formatter import format_post
from publisher.queue_manager import get_next_post, mark_posted
import config

BOT_TOKEN = os.getenv("BOT_TOKEN") or config.BOT_TOKEN
CHANNEL_ID = os.getenv("CHANNEL_ID") or config.CHANNEL_ID

bot = Bot(token=BOT_TOKEN)

async def publish_next():
    post = await get_next_post()
    if not post:
        return

    post_id, text, image_path, source = post
    caption = format_post(text, source)

    try:
        if image_path:
            with open(image_path, "rb") as photo:
                await bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=caption, parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=caption, parse_mode=ParseMode.HTML)
        await mark_posted(post_id)
        print(f"Published post {post_id} to {CHANNEL_ID}")
    except Exception as e:
        print(f"Publish error: {e}")
