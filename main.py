from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import random
import string
import sqlite3


owner = 6521329614
admin = ['6521329614','6716393007']

conn =  sqlite3.connect('database.db')
cursor = conn.cursor()

# cursor.execute('DELETE FROM admins')
# conn.commit()

for id in admin:
    cursor.execute(f'insert into admins (id) values ("{id}")')
    conn.commit()

admin_list = []
def updater():
    for item in cursor.execute('select * from admins').fetchall():
        if item[0] not in admin_list:
            admin_list.append(item[0])
updater()

def add_admin(id):
    cursor.execute(f'insert into admins (id) values ("{id}")')
    conn.commit()  
    updater() 


def fetch_codes():
    cursor.execute('SELECT * FROM codes')    
    print(cursor.fetchall())
        
# fetch_codes()

def checker(file_id):
    for item in cursor.execute('select * from codes').fetchall():
        if file_id == item[1]:
            return [False,item[0]]
    else:
        return([True])
    
def file_code(length=5):
    characters = string.ascii_lowercase + string.digits
    code = ''.join(random.choices(characters, k=length))
    
    for item in cursor.execute('select * from codes').fetchall():
        if code == item[0]:
            file_code()
    else:
        return code
    
async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text:
        file_code = update.message.text
        list_codes = cursor.execute('select code from codes').fetchall()
        last_list = list(map(lambda x : x[0],list_codes))
        if file_code in last_list:
            data_list = cursor.execute(f'select file_id,type from codes where code == "{file_code}"').fetchall()[0]
            if data_list[1] == 'video':
                await update.message.reply_video(data_list[0])
            else:
                await update.message.reply_document(data_list[0])
    elif update.message.video and update.message.chat.id in admin_list:
        file_id = update.message.video.file_id
        code_file = file_code()
        cursor.execute(f'INSERT INTO codes (code,file_id,type) VALUES ("{code_file}","{file_id}","video")')
        conn.commit()
        await update.message.reply_text(f'فایل با موفقیت ثبت شد کد فایل برای کپی کردن کلیک کنید: \n `{code_file}`',parse_mode='MarkdownV2')
    elif update.message.document and update.message.chat.id in admin_list:
        file_id = update.message.document.file_id
        code_file = file_code()
        cursor.execute(f'INSERT INTO codes (code,file_id,type) VALUES ("{code_file}","{file_id}","document")')
        conn.commit()
        await update.message.reply_text(f'فایل با موفقیت ثبت شد کد فایل برای کپی کردن کلیک کنید: \n `{code_file}`',parse_mode='MarkdownV2')
        
    else:
        pass

TOKEN = "7110280378:AAH3Zg9379OOYwE_hs22yP8SuIIJrhTZEfo"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_all_messages))

app.run_polling()
