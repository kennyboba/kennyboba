import os
from telegram.ext import Application, MessageHandler, CommandHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")
FILE_PATH = "hits.txt"

async def save(update, context):
    msg = update.message
    text = msg.text or msg.caption or ""
    line = f"[{msg.date}] {text}\n"
    
    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(line)

async def get_file(update, context):
    if os.path.exists(FILE_PATH):
        await update.message.reply_document(FILE_PATH)
        os.remove(FILE_PATH)
        await update.message.reply_text("File sent and cleared. Fresh start for new hits.")
    else:
        await update.message.reply_text("No hits logged yet.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, save))
    app.add_handler(CommandHandler("get", get_file))
    print("Logger bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
