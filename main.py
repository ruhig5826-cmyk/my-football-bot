import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from collector.telegram_listener import start_listener
from collector.rss_poller import poll_rss
from publisher.bot_publisher import publish_next
from publisher.queue_manager import init_db
from processing.translator import setup_translation


async def main():
    init_db()
    setup_translation()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(poll_rss, "interval", minutes=5, id="rss_poll")
    scheduler.add_job(publish_next, "interval", minutes=3, id="publish_next")
    scheduler.start()

    print("🤖 Football Bot started!")
    await start_listener()


if __name__ == "__main__":
    asyncio.run(main())
