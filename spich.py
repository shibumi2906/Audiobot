import os
import openai
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = '6593004563:AAF6_VdpPQKQ-hYjsAcrz6GBwuVnx_CPwFc'
OPENAI_API_KEY = 'sk-SeA46H6qerPo06VdVK2HxMabiqq7maWT'

openai.api_key = OPENAI_API_KEY


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Отправьте мне аудио сообщение, и я преобразую его в текст и отправлю в ChatGPT.')


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    audio_file = await update.message.voice.get_file()
    audio_file_path = await audio_file.download('voice.ogg')

    # Конвертируем OGG в WAV
    audio = AudioSegment.from_ogg(audio_file_path)
    audio.export("voice.wav", format="wav")

    # Используем speech_recognition для распознавания речи
    recognizer = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")

    await update.message.reply_text(f'Распознанный текст: {text}')

    # Отправляем текст в ChatGPT
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=text,
        max_tokens=150
    )

    await update.message.reply_text(f'Ответ ChatGPT: {response.choices[0].text.strip()}')


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, handle_audio))

    application.run_polling()


if __name__ == '__main__':
    main()
