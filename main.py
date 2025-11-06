import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 🔹 LOG SOZLAMALARI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Environment variables orqali token va API kalit
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔹 Google Gemini AI konfiguratsiyasi
genai.configure(api_key=GEMINI_API_KEY)

# 🔹 Mavjud va ishlaydigan modelni ishlatish
# ListModels orqali aniqlangan model: gemini-1.5
model = genai.GenerativeModel("gemini-1.5")

# 🔹 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "👋 Salom! Men Gemini AI botman.\n"
            "Menga mavzu yuboring va men sizga slayd/referat tayyorlab beraman.\n\n"
            "Masalan: 'O'zbekistonning iqlimi haqida referat'."
        )

# 🔹 Asosiy AI javobi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    topic = update.message.text
    logger.info(f"Foydalanuvchi mavzuni yubordi: {topic}")

    prompt = (
        f"Sizga mavzu berildi: {topic}\n"
        "Iltimos, bu mavzuda qisqa va to‘liq slayd/referat tayyorlang. "
        "Har bir bo‘limni raqam bilan ajrating va soddalashtirilgan tarzda yozing."
    )

    try:
        # generate_text metodidan foydalanamiz, generate_content ba'zan eski versiyalarda ishlamaydi
        response = model.generate_text(prompt)
        ai_text = response.text if hasattr(response, "text") else "❌ Javob olinmadi."
        await update.message.reply_text(ai_text)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi. Keyinroq urinib ko‘ring.")

# 🔹 Asosiy ishga tushirish
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot ishga tushdi... (Gemini AI bilan)")
    application.run_polling()

if __name__ == "__main__":
    main()
