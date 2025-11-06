import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 🔹 Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 API kalitlari
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔹 Gemini AI sozlamasi
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5")

# 🔹 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men Gemini AI botman. "
        "Menga savol yoki mavzu yozing, men AI yordamida javob beraman."
    )

# 🔹 Foydalanuvchi xabarini AI ga yuborish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logger.info(f"Foydalanuvchi xabar yubordi: {user_text}")

    try:
        response = model.generate_text(user_text)
        ai_text = response.text if hasattr(response, "text") else "AI javob bera olmadi 😔"
        await update.message.reply_text(ai_text)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring.")

# 🔹 Botni ishga tushirish
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    main()
