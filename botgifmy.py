import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Вставьте ваш токен от Telegram Bot API
TOKEN = 'my token'
bot = telebot.TeleBot(TOKEN)

# Путь к созданному GIF-файлу
GIF_PATH = 'countdown.gif'

# Функция для создания клавиатуры с кнопкой
def create_start_timer_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton('Start Timer')
    keyboard.add(start_button)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    welcome_text = "Нажмите кнопку ниже, чтобы запустить таймер:"
    bot.send_message(chat_id, welcome_text, reply_markup=create_start_timer_keyboard())

@bot.message_handler(func=lambda message: message.text == "Start Timer")
def start_timer(message):
    chat_id = message.chat.id
    with open(GIF_PATH, 'rb') as gif_file:
        bot.send_animation(chat_id, gif_file, caption="У вас есть 2 минуты на ответ.")

# Запуск бота
bot.polling()


