from telegram import Update
from telegram.ext import ContextTypes

from entities.dto import MessageDTO, UserDTO
from use_cases.exchange_request import ExchangeRequestInteractor
from use_cases.report import ReportInteractor
from use_cases.start import StartInteractor
from use_cases.uncategorized import UncategorizedInteractor
from utils.database import db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    request_data = UserDTO(
        id=update.effective_user.id,
        first_name=update.effective_user.first_name,
        username=update.effective_user.username,
        full_name=update.effective_user.full_name
    )
    reply_text = await StartInteractor(db).execute(request_data)
    await update.message.reply_markdown(reply_text)


async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    request_data = MessageDTO(
        id=update.message.message_id,
        chat_id=update.message.chat_id,
        external_user_id=update.effective_user.id,
        text=update.message.text,
    )
    await update.message.reply_text(await ExchangeRequestInteractor(db).execute(request_data))


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    request_data = UserDTO(
        id=update.effective_user.id,
        first_name=update.effective_user.first_name,
        username=update.effective_user.username,
        full_name=update.effective_user.full_name
    )
    # fixme: по хорошему reply_html + jinja, но нужно понимать как выглядит
    await update.message.reply_text(await ReportInteractor(db).execute(request_data))


async def uncategorized_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    request_data = MessageDTO(
        id=update.message.message_id,
        chat_id=update.message.chat_id,
        external_user_id=update.effective_user.id,
        text=update.message.text,
    )
    reply_text = await UncategorizedInteractor(db).execute(request_data)
    await update.message.reply_text(reply_text)
