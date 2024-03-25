from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes
import pygame

pygame.init()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Wyślij komendę aby uruchomić dźwięk")

async def echo(update: Update, context: CallbackContext) -> None:
    text_received = update.message.text.lower()
    valid_sounds = ["cheese"]

    if text_received in valid_sounds:
        mp3_file = f'{text_received}.mp3'
        try:
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            await update.message.reply_text(f'Odtworzono plik MP3: {text_received}')
        except Exception as e:
            await update.message.reply_text("Wystąpił błąd przy odtwarzaniu pliku: " + str(e))
    else:
        await update.message.reply_text("Nie rozpoznaję tej komendy, Spróbuj coś z tej listy: " + ", ".join(valid_sounds))

def main() -> None:
    application = Application.builder().token("TELEGRAM_API").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()

if __name__ == '__main__':
    main()