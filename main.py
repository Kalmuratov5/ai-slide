import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 🔹 Log sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Token va API kalitlari
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔹 Gemini AI konfiguratsiyasi
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5")  # Ishlaydigan model

# 🔹 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men Gemini AI botman.\n"
        "Mavzu yuboring, men sizga slayd yoki referat tayyorlab beraman.\n"
        "Masalan: 'O'zbekistonning iqlimi haqida referat'."
    )

# 🔹 AI javobini olish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    logger.info(f"Foydalanuvchi mavzuni yubordi: {topic}")

    prompt = (
        f"Sizga mavzu berildi: {topic}\n"
        "Iltimos, bu mavzuda qisqa va to‘liq slayd yoki referat tayyorlang. "
        "Har bir bo‘limni raqam bilan ajrating va soddalashtirilgan tarzda yozing."
    )

    try:
        response = model.generate_text(prompt)
        ai_text = response.text if hasattr(response, "text") else "❌ Javob olinmadi."
        await update.message.reply_text(ai_text)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi. Keyinroq urinib ko‘ring.")

# 🔹 Botni ishga tushirish
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot ishga tushdi... (Gemini AI bilan)")
    application.run_polling()  # Updater ishlatilmaydi

if __name__ == "__main__":
    main()
