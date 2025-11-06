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

# 🔹 TOKENLAR (Environment Variables orqali)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    logger.error("❌ TELEGRAM_BOT_TOKEN yoki GEMINI_API_KEY o'rnatilmagan!")
    exit(1)

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
