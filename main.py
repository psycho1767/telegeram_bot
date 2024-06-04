# 7110280378:AAH3Zg9379OOYwE_hs22yP8SuIIJrhTZEfo

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'سلام {update.effective_user.first_name}')


app = ApplicationBuilder().token("7110280378:AAH3Zg9379OOYwE_hs22yP8SuIIJrhTZEfo").build()

app.add_handler(CommandHandler("سلام", hello))

app.run_polling()