import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# Logger sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEN_API_KEY = os.getenv("GEN_API_KEY")

# Gemini API orqali javob olish funksiyasi
def get_gemini_response(question: str) -> str:
    url = "https://api.generativeai.googleapis.com/v1beta2/models/text-bison-001:generateText"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEN_API_KEY}"
    }
    payload = {
        "prompt": question,
        "temperature": 0.7,
        "maxOutputTokens": 200
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("candidates", [{}])[0].get("output", "Kechirasiz, javob topilmadi.")
    except Exception as e:
        logging.error(f"Gemini API xatosi: {e}")
        return "Xatolik yuz berdi, iltimos keyinroq urinib ko'ring."

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men Gemini API bilan ishlaydigan oddiy chatbotman.\nSavolingizni yozing va men javob beraman."
    )

# Foydalanuvchi xabarini qabul qilish va javob berish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    answer = get_gemini_response(question)
    await update.message.reply_text(answer)

# Asosiy funksiya
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Botni ishga tushurish
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
