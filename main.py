import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai  # Gemini API SDK

# Telegram va Gemini API kalitlarini o'rnatish
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKENINGIZNI_BUYERGA"
GEN_API_KEY = "GEMINI_API_KEY_BUYERGA"

# Gemini mijozini yaratish
client = genai.Client(api_key=GEN_API_KEY)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga savol berishingiz mumkin.")

# Foydalanuvchi xabarini qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Gemini API ga so'rov yuborish
    response = client.responses.create(
        model="gemini-1.5",
        input=user_text
    )

    # API javobini foydalanuvchiga yuborish
    await update.message.reply_text(response.output_text)

# Asosiy dastur
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()
