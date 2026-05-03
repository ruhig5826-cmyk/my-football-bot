import feedparser
from publisher.queue_manager import enqueue_post
from processing.filter import is_relevant
from processing.translator import translate_text
from collector.deduplicator import is_duplicate, mark_seen

RSS_FEEDS = [
    "https://rss.dw.com/xml/DK/sport",
    "https://www.goal.com/feeds/en/34.xml",
    "https://www.espn.com/espn/rss/football/news",
]


def fetch_feed_items():
    posts = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            text = f"{title}\n{summary}\n{link}"
            posts.append({"text": text, "source": feed.feed.get("title", "RSS")})
    return posts


async def poll_rss():
    items = fetch_feed_items()
    for item in items:
        text = item["text"]
        source = item["source"]
        if not text or len(text.strip()) < 20:
            continue
        if is_duplicate(text):
            continue
        if not is_relevant(text):
            continue
        mark_seen(text)
        translated = await translate_text(text)
        await enqueue_post(translated, None, source)
