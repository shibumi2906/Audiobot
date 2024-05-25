import os
import openai
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = '6593004563:AAF6_VdpPQKQ-hYjsAcrz6GBwuVnx_CPwFc'
OPENAI_API_KEY = 'sk-SeA46H6qerPo06VdVK2HxMabiqq7maWT'

openai.api_key = OPENAI_API_KEY


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправьте мне аудио сообщение, и я преобразую его в текст и отправлю в ChatGPT.')


def handle_audio(update: Update, context: CallbackContext) -> None:
    audio_file = update.message.voice.get_file().download('voice.ogg')

    # Конвертируем OGG в WAV
    audio = AudioSegment.from_ogg(audio_file)
    audio.export("voice.wav", format="wav")

    # Используем speech_recognition для распознавания речи
    recognizer = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")

    update.message.reply_text(f'Распознанный текст: {text}')

    # Отправляем текст в ChatGPT
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=text,
        max_tokens=150
    )

    update.message.reply_text(f'Ответ ChatGPT: {response.choices[0].text.strip()}')


def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.voice, handle_audio))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
