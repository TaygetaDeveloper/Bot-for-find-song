import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI


# ----------------------------------------
# CONFIG
# ----------------------------------------
TELEGRAM_TOKEN = "YOUR_TELEGRAM_API_CODE"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

client = OpenAI(api_key=OPENAI_API_KEY)


# ----------------------------------------
# START
# ----------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🎵\n"
        "Опиши песню (слова, сюжет клипа, настроение, фразы), "
        "и я попробую найти, что это за трек."
    )


# ----------------------------------------
# MAIN LOGIC
# ----------------------------------------
async def find_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    prompt = (
        f"Пользователь описывает песню: {user_text}.\n"
        f"Определи, какая это песня. Дай исполнителя, название "
        f"и объясни, почему именно она. Если есть несколько вариантов — перечисли."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


# ----------------------------------------
# RUN BOT
# ----------------------------------------
def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_song))

    print("Bot started!")
    app.run_polling()


if __name__ == "__main__":
    main()
