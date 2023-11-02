import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, Application

from routing import command_handlers, message_handlers
from settings import Settings
from utils.database import db
from utils.migration import run_migration

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def post_init(app: Application) -> None:
    await app.bot.set_my_commands([('start', 'Starts the bot')])

    # fixme: решил не использовать алхимию, из-за этого не успел прикрутить алембик/аналог
    await run_migration(db)


async def post_stop(app: Application) -> None:
    await db.close_connection()


def run():
    settings = Settings()

    app = ApplicationBuilder().token(settings.tg_bot_token).post_init(post_init).post_stop(post_stop).build()
    for pattern, func, _ in command_handlers:
        app.add_handler(CommandHandler(pattern, func))

    for pattern, func, _ in message_handlers:
        app.add_handler(MessageHandler(pattern, func))

    app.run_polling(allowed_updates=Update.MESSAGE)


if __name__ == '__main__':
    run()
