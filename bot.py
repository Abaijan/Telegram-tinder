from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


async def start(update, context):
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)


async def hello(update, context):
    await send_text(update, context, "*Привет*")
    await send_text(update, context, "Как дела?")
    await send_text(update, context, "Вы написали " + update.message.text)
    await send_photo(update, context, "avatar_main")
    await send_text_buttons(update, context, "Go to run?", {
        "start": "Go to Start",
        "stop": "Go to Stop"
    })


async def hello_buttonz(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "*Procces is run*")
    else:
        await send_text(update, context, "Priccess is stoped")


app = ApplicationBuilder().token("7416453490:AAElVYwjJgnj1FvcrohB-GdQMynjKp1Zx6I").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_buttonz))
app.run_polling()
