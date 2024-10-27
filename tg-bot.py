import telebot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests
import json
import time
import types

# Укажите токен и ссылки
token = '7866617284:AAHDOfPQJdKmufOdRgFza6XA8ZWRHPeA_Yc'
signUpUrl = 'https://sergeymorykov-tg-web-app-react-72ec.twc1.net/signup'
eventsUrl = 'https://sergeymorykov-tg-web-app-react-72ec.twc1.net/events'
profilesUrl = 'https://sergeymorykov-tg-web-app-react-72ec.twc1.net/user-list'
# Создаем экземпляр бота
bot = telebot.TeleBot(token)

# Функция для проверки, зарегистрирован ли пользователь
def check_users_presence(chat_id):
    presence = False
    # Здесь добавьте свою логику для проверки пользователя
    return presence

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    data = message.web_app_data.data  # This is the JSON string sent from the web app
    print(f"Data: {data}")
"""
@bot.message_handler(commands=['start'])
def handle_start(message):
    web_app_url = signUpUrl  # Замените на URL вашего Web App
    web_app = types.WebAppInfo(url=web_app_url)

    # Создаем кнопку с типом web_app и привязываем к ней Web App URL
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    web_app_button = types.KeyboardButton(text="Open Web App", web_app=web_app)
    keyboard.add(web_app_button)

    bot.send_message(message.chat.id, "Нажмите кнопку ниже для открытия Web App:", reply_markup=keyboard)
"""

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id

    # URL вашего API
    url = 'http://localhost:5000/last_chat_id'  # Замените на ваш адрес

    # Данные, которые вы хотите отправить
    data = {
        'last_id': str(chat_id)  # Замените на ваше имя поля и значение
    }

    # Отправка POST-запроса с JSON
    response = requests.post(url, json=data)

    # Создаем клавиатуру с кнопками
    markup = InlineKeyboardMarkup()
    
    # Кнопка для регистрации
    markup.add(InlineKeyboardButton("📝 Sign up", web_app=WebAppInfo(url=signUpUrl)))
    
    # Кнопка для просмотра событий
    markup.add(InlineKeyboardButton("📅 View Events", web_app=WebAppInfo(url=eventsUrl)))
    markup.add(InlineKeyboardButton("📅 View list profile", web_app=WebAppInfo(url=profilesUrl)))
    bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь или посмотрите события", reply_markup=markup)

    if message.web_app_data and message.web_app_data.data:
        try:
            data = json.loads(message.web_app_data.data)
            print(f"Data: {data}")
            bot.send_message(chat_id, 'Спасибо за обратную связь')
            bot.send_message(chat_id, 'Вашe Имя: ' + data.get('country', 'Не указана'))
            bot.send_message(chat_id, 'Фамилия: ' + data.get('street', 'Не указана'))

            time.sleep(3)  # Задержка перед отправкой сообщения
            bot.send_message(chat_id, 'Всю информацию вы получите в этом чате')
        except json.JSONDecodeError as e:
            print(f"Ошибка разбора JSON: {e}")

# Запуск бота
bot.polling()