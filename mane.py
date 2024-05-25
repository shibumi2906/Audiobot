import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from pydub import AudioSegment
import openai
import requests
import whisper

# Указание пути к ffmpeg
ffmpeg_path = r'C:\Users\IMOE001\Documents\GitHub\Audiobot\fanv\ffmpeg-7.0\bin\ffmpeg.exe'
AudioSegment.converter = ffmpeg_path

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Ваши токены
TELEGRAM_TOKEN = '6593004563:AAF6_VdpPQKQ-hYjsAcrz6GBwuVnx_CPwFc'
OPENAI_API_KEY = 'sk-SeA46H6qerPo06VdVK2HxMabiqq7maWT'

openai.api_key = OPENAI_API_KEY

# Попробуйте импортировать whisper из альтернативного пакета
try:
    model = whisper.load_model("base")
except ImportError:
    logger.error("Could not import whisper. Please make sure it is installed.")
    raise
except Exception as e:
    logger.error("Error loading Whisper model: %s", e)
    raise

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Отправьте мне аудио сообщение, и я преобразую его в текст и отправлю в ChatGPT.')

# Обработчик аудио сообщений
async def audio(update: Update, context: CallbackContext) -> None:
    try:
        file = await update.message.voice.get_file()
        file_path = file.file_path

        # Скачивание файла вручную
        local_file_path = 'audio.ogg'
        response = requests.get(file_path)
        with open(local_file_path, 'wb') as f:
            f.write(response.content)

        # Конвертация ogg в wav
        audio = AudioSegment.from_file(local_file_path)
        audio.export('audio.wav', format='wav')

        # Преобразование аудио в текст с помощью Whisper
        result = model.transcribe('audio.wav')
        text = result['text']
        await update.message.reply_text(f"Распознанный текст: {text}")

        # Отправка текста в ChatGPT
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            max_tokens=150
        )
        reply_text = response.choices[0].text.strip()
        await update.message.reply_text(reply_text)
    except Exception as e:
        logger.error("Error processing audio message: %s", e)
        await update.message.reply_text('Произошла ошибка при обработке вашего аудио сообщения. Пожалуйста, попробуйте еще раз.')

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, audio))

    application.run_polling()

if __name__ == '__main__':
    main()






