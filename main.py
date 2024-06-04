from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import random
import string

def file_code(length=5):
    characters = string.ascii_lowercase + string.digits
    code = ''.join(random.choices(characters, k=length))
    return code

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text:
        await update.message.reply_text(f'شما یک پیام متنی ارسال کردید: {update.message.text}')
    elif update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_video(video=file_id, caption=f'کد فایل : {file_code()}')
    elif update.message.document:
        file_id = update.message.document.file_id
        await update.message.reply_document(document=file_id, caption=f'کد فایل : {file_code()}')
    else:
        print(update.message)

TOKEN = "7110280378:AAH3Zg9379OOYwE_hs22yP8SuIIJrhTZEfo"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_all_messages))

app.run_polling()
