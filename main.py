import logging
import os
import uuid
from textwrap import dedent

from dotenv import load_dotenv
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f"Hello {update.effective_user.first_name}. I'm a bot, please talk to me!",
    )


def get_meet_handler(meet_name_prefix):

    async def meet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        meet_url = f"https://meet.jit.si/{meet_name_prefix}-{str(uuid.uuid4()).replace('-', '')}"
        reply_msg = dedent(f"""
            <b>💎 Start & join meetings 🍻 for free 🔓 </b>
            🕶 Premium video calls. Now available to everyone! 😁
            👌🏼 <i>No account needed</i> 👋🏻
            <a href='{meet_url}'>👉🏻 Join meeting 👈🏻</a>
            """)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="👉🏻 Join meeting 👈🏻", url=meet_url)],
        ])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_msg,
            reply_markup=reply_markup,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    return meet_handler


def main():
    meet_name_prefix = os.getenv("MEET_NAME_PREFIX")
    tg_token = os.getenv("TG_BOT_TOKEN")
    application = ApplicationBuilder().token(tg_token).build()
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(
        CommandHandler("meet", get_meet_handler(meet_name_prefix)))
    application.run_polling()


if __name__ == "__main__":
    load_dotenv()
    main()
