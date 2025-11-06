import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import openai
import io

# Telegram va OpenAI API kalitlari
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men Gemini AI botman. Siz menga matn yuborishingiz mumkin.\n"
        "Agar sizga slayd kerak bo‘lsa, matnni yuboring va men .pptx tayyorlayman."
    )

# Matn yuborilganda ishlaydi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Gemini AI orqali javob olish
    try:
        response = openai.ChatCompletion.create(
            model="gemini-1.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_text = response.choices[0].message.content
    except Exception as e:
        ai_text = f"AI bilan bog'lanishda xatolik: {e}"

    await update.message.reply_text(f"Gemini AI javobi:\n{ai_text}")

    # Slayd yaratish
    prs = Presentation()
    slide_layout = prs.slide_layouts[5]  # bo'sh slayd
    slide = prs.slides.add_slide(slide_layout)

    # Sarlavha qo'shish
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = "Gemini AI Bot Slaydi"
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(0, 102, 204)

    # AI javobini qo'shish
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(4))
    content_frame = content_box.text_frame
    content_frame.text = ai_text
    content_frame.paragraphs[0].font.size = Pt(20)
    content_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)

    # Faylni yuborish
    pptx_stream = io.BytesIO()
    prs.save(pptx_stream)
    pptx_stream.seek(0)
    await update.message.reply_document(document=pptx_stream, filename="Gemini_Slide.pptx")

# Main funksiyasi
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
