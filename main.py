from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import random
import string
import sqlite3

conn =  sqlite3.connect('database.db')
cursor = conn.cursor()


def fetch_codes():
    cursor.execute('SELECT * FROM codes')
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
        
fetch_codes()
            
def file_code(length=5):
    characters = string.ascii_lowercase + string.digits
    code = ''.join(random.choices(characters, k=length))
    return code

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text:
        await update.message.reply_text(f'شما یک پیام متنی ارسال کردید: {update.message.text}')
    elif update.message.video:
        file_id = update.message.video.file_id
        file_code = file_code()
        await cursor.execute(f'INSERT INTO codes (code,file_id,type) VALUES ({file_code},{file_id},"video")')
        await update.message.reply_text(f'فایل با موفقیت ثبت شد کد فایل: \n `{file_code}`')

        fetch_codes()
    elif update.message.document:
        file_id = update.message.document.file_id
        file_code = file_code()
        await cursor.execute(f'INSERT INTO codes (code,file_id,type) VALUES ({file_code},{file_id},"document")')
        await update.message.reply_text(f'فایل با موفقیت ثبت شد کد فایل: \n `{file_code}`')
        
        fetch_codes()
    else:
        print(update.message)

TOKEN = "7110280378:AAH3Zg9379OOYwE_hs22yP8SuIIJrhTZEfo"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_all_messages))

app.run_polling()
