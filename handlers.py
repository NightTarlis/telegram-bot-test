from telegram import Update
from telegram.ext import ContextTypes

from use_cases.exchange_request import ExchangeRequestInteractor
from use_cases.report import ReportInteractor
from use_cases.start import StartInteractor
from use_cases.uncategorized import UncategorizedInteractor
from utils.database import db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_text = await StartInteractor(db).execute(update.effective_user)
    await update.message.reply_markdown(reply_text)


async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        await ExchangeRequestInteractor(db).execute(update.message, update.effective_user.id)
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(await ReportInteractor(db).execute(update.effective_user.id))


async def uncategorized_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_text = await UncategorizedInteractor(db).execute(
        update.message.id, update.message.chat_id, update.message.text, update.effective_user.id
    )
    await update.message.reply_text(reply_text)
