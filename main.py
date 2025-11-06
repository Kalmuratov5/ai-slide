import logging
import asyncio
import os
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 🔹 LOG SOZLAMALARI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 TOKENLAR (shu yerda yozilgan)
TELEGRAM_BOT_TOKEN = "7079998022:AAEcMbdT-1wIpiqQqqmVx7B_cOy07vQ7vno"
GEMINI_API_KEY = "AIzaSyBJd1xvPOnLKsbiRuy88rJbFPG5UO-2hW0"

# 🔹 GOOGLE GEMINI ULANISH
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🔹 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "👋 Salom! Men Gemini AI botman.\n"
            "Menga savolingizni yozing yoki mavzuni yuboring.\n\n"
            "Masalan: 'O'zbekistonning iqlimi haqida ma'lumot'."
        )

# 🔹 Asosiy AI javobi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    logger.info(f"Foydalanuvchi yozdi: {user_text}")

    try:
        response = model.generate_content(user_text)
        ai_reply = response.text if hasattr(response, "text") else "❌ Javob olinmadi."
        await update.message.reply_text(ai_reply)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi. Keyinroq urinib ko‘ring.")

# 🔹 Asosiy ishga tushirish funksiyasi
async def main():
    os.environ["TZ"] = "Asia/Tashkent"
    pytz.timezone("Asia/Tashkent")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot ishga tushdi... (Railway versiyasi)")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
