import aiohttp
from PIL import Image, ImageDraw, ImageFont
import io
import os

UNSPLASH_KEY = os.getenv("UNSPLASH_KEY")
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", "⚽ @YourChannel")

async def get_image(msg, text: str) -> str | None:
    if getattr(msg, "media", None):
        try:
            path = f"/tmp/img_{msg.id}.jpg"
            await msg.download_media(path)
            return add_watermark(path)
        except Exception:
            pass

    keywords = extract_keywords(text)
    image_path = await fetch_unsplash_image(keywords)
    if image_path:
        return add_watermark(image_path)

    return None

async def fetch_unsplash_image(query: str) -> str | None:
    if not UNSPLASH_KEY:
        return None
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                data = await r.json()
                img_url = data.get("urls", {}).get("regular")
                if not img_url:
                    return None
                async with session.get(img_url) as ir:
                    content = await ir.read()
                    path = f"/tmp/unsplash_{abs(hash(query))}.jpg"
                    with open(path, "wb") as f:
                        f.write(content)
                    return path
    return None


def add_watermark(image_path: str) -> str:
    try:
        img = Image.open(image_path).convert("RGBA")
        txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        font = ImageFont.load_default()
        text = WATERMARK_TEXT
        margin = 10
        text_width, text_height = draw.textsize(text, font=font)
        position = (img.width - text_width - margin, img.height - text_height - margin)
        draw.text(position, text, fill=(255, 255, 255, 180), font=font)
        watermarked = Image.alpha_composite(img, txt).convert("RGB")
        out_path = image_path.replace(".jpg", "_wm.jpg")
        watermarked.save(out_path, quality=85)
        return out_path
    except Exception:
        return image_path


def extract_keywords(text: str) -> str:
    sports_keywords = ["football", "soccer", "goal", "match", "transfer", "player", "coach", "stadium"]
    words = [w.strip(".,!?:;()[]\"").lower() for w in text.split()]
    found = [w for w in words if w in sports_keywords]
    return " ".join(found[:3]) if found else "football match"
