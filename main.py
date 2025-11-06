import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai  # google‑genai SDK

# 🔹 Log sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Token va API kalitlari
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔹 Gemini API mijozini sozlash
client = genai.Client(api_key=GEMINI_API_KEY)

# 🔹 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men Gemini‑chatbotman. Siz menga savol yozing, men AI yordamida javob beraman."
    )

# 🔹 Matn yuborilganda ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logger.info(f"Foydalanuvchi yubordi: {user_text}")

    try:
        # Gemini modeliga so‘rov yuborish
        result = client.chat.completions.create(
            model="gemini‑2.5‑flash",  # model nomi sizda mosligini tekshiring
            messages=[{"role": "user", "content": user_text}]
        )
        ai_text = result.choices[0].message.content
        await update.message.reply_text(ai_text)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring.")

# 🔹 Main funksiyasi
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    main()
