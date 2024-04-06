import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
)
from commentsbot.config import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_chat is not None
    id = update.effective_chat.id

    await context.bot.send_message(chat_id=id, text=f"Chat ID: {id}")


async def chat_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_user is not None
    assert update.effective_chat is not None

    if update.effective_chat.id == config.SUBSCRIBERS_CHAT_ID:
        return

    member = await context.bot.get_chat_member(
        config.SUBSCRIBERS_CHAT_ID, update.effective_user.id
    )

    if member.status == member.MEMBER:
        await context.bot.approve_chat_join_request(
            update.effective_chat.id, update.effective_user.id
        )


async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_message is not None
    assert update.effective_chat is not None

    if str(update.effective_chat.id) != config.SUBSCRIBERS_CHAT_ID:
        return

    if update.effective_message.left_chat_member is not None:
        id = update.effective_message.left_chat_member.id

        for chat_id in config.PAID_CHATS:
            await context.bot.unban_chat_member(chat_id, id)


def main():
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("get_id", get_id))
    application.add_handler(ChatJoinRequestHandler(chat_join))
    application.add_handler(MessageHandler(None, leave))

    application.run_polling()
