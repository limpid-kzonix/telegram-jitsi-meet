import logging
import os
import uuid
import re

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
from textwrap import dedent

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {update.effective_user.first_name}. I'm a bot, please talk to me!")


async def meet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    # TODO: implement cli-like flag's parsiing (e.g --name)
    chat_name = next(iter(args), update.effective_chat.title or update.effective_chat.id)
    meet_name = f"{chat_name}---{str(uuid.uuid4())}"
    meet_name = re.sub('[^A-Za-z0-9]', '-', meet_name)
    meet_url = f"https://meet.jit.si/{meet_name}"
    reply_msg = dedent(f"""
        ❄️🌲☃️❄️🌲❄️☃️🌲❄️

        <b>✨✨{chat_name}✨✨</b>
        <b>📢Start & join🤳</b>
        🕶Premium video calls.
        💖Now available to everyone!
        👌🏼<i>No account needed</i>

        <a href='{meet_url}'> 🔗 Join meeting</a>
        """)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='👉🏻 Join 👈🏻', url=meet_url)],
    ])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_msg, reply_markup=reply_markup, parse_mode='HTML', disable_web_page_preview=True)


def main():
    tg_token = os.getenv("TG_BOT_TOKEN")
    application = ApplicationBuilder().token(tg_token).build()
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('meet',  meet_handler))
    application.run_polling()


if __name__ == '__main__':
    load_dotenv()
    main()
