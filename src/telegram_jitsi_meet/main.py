import argparse
import logging
import os
import re
import uuid
from textwrap import dedent

from dotenv import load_dotenv
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)


parser = argparse.ArgumentParser(
    usage="/meet [-h] [-n [NAME ...]] [meet_name ...]", description="Jitsy Meet Bot"
)
parser.add_argument("-n", "--name", nargs="*", help="Specify 'name' argument.")
parser.add_argument("meet_name",
                    type=str,
                    nargs="*",
                    help="An optional name argument")



async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Hello {update.effective_user.first_name}. I'm a bot, please talk to me!"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
    )


def is_valid(name):
    if name is None:
        return False
    elif type(name) is list:
        return len(name) != 0
    elif type(name) is str:
        return name.strip() != ""
    else:
        return True


async def parse_args(context_args):
    input_args = list(map(lambda x: x.replace("—", "--"), context_args or []))
    names = []
    try:
        ns = parser.parse_args(input_args)
        names = [ns.name, ns.meet_name]
    except BaseException as e:
        logging.error(e.args)

    names = list(filter(is_valid, names))
    names = list(map(lambda x: " ".join(x), names))
    return names


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = dedent(
        f"""
        {parser.format_help()}
        """
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_msg)


async def meet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = await parse_args(context.args)
    chat_name = next(
        iter(names),
        update.effective_chat.title or update.effective_chat.id,
    )
    meet_name = f"{chat_name}---{str(uuid.uuid4())}"
    meet_name = re.sub("[^A-Za-z0-9]", "-", meet_name)
    meet_url = f"https://meet.jit.si/{meet_name}"
    reply_msg = dedent(f"""
        <b>✨✨{chat_name}✨✨</b>
        <b>📢Start & join🤳</b>
        🕶Premium video calls.
        💖Now available to everyone!
        👌🏼<i>No account needed</i>

        <a href='{meet_url}'> 🔗 Join meeting</a>
        """)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="👉🏻 Join 👈🏻", url=meet_url)],
    ])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_markup=reply_markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


def start():
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    application = ApplicationBuilder().token(tg_token).build()
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("meet", meet_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.run_polling()

if __name__ == "__main__":
    start()


