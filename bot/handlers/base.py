from db import start_db, shutdown_db
from utils import log_action


async def on_startup():
    await start_db()
    log_action().info("Bot started")


async def on_shutdown():
    await shutdown_db()
    log_action().info("Bot is Disabled")
