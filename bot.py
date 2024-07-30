from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        "start": "запустить",
        "gpt": "Общение с чатом GPT",
        "profile": "генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",

    })

async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question("напиши четкий и короткий ответ на следующий вопрос : ", text)
    await send_text(update, context, answer)


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
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


dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token="gpt:61rNHlA6YvvAAhkXHkjMJFkblB3T1ra23XYN7pLIKmOsUDqe")

app = ApplicationBuilder().token("7416453490:AAElVYwjJgnj1FvcrohB-GdQMynjKp1Zx6I").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_buttonz))
app.run_polling()
