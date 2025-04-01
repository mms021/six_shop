import asyncio, json, os
from datetime import datetime

import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Конфигурация
BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
WEBAPP_URL = os.getenv('TG_WEB_APP_URL')
TG_SUPPORT_USERNAME = os.getenv('TG_SUPPORT_USERNAME')
TG_SUPPORT_PHONE = os.getenv('TG_SUPPORT_PHONE')
TG_SUPPORT_EMAIL = os.getenv('TG_SUPPORT_EMAIL')
TG_SUPPORT_ADDRESS = os.getenv('TG_SUPPORT_ADDRESS')
TG_SUPPORT_WORK_TIME = os.getenv('TG_SUPPORT_WORK_TIME')
BOT_WEBAPP_NAME = os.getenv('TG_BOT_WEBAPP_NAME', 'sixoclocktestbot')  # Добавляем имя веб-приложения

bot = telebot.TeleBot(BOT_TOKEN)

def get_main_keyboard():
    """Создает основную клавиатуру бота"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    shop_button = KeyboardButton('🛍 Магазин')
    info_button = KeyboardButton('ℹ️ Информация')
    contact_button = KeyboardButton('📞 Поделиться контактом', request_contact=True)
    support_button = KeyboardButton('🆘 Поддержка')
    
    keyboard.row(shop_button)
    keyboard.row(info_button, support_button)
    keyboard.row(contact_button)
    return keyboard

def get_webapp_keyboard():
    """Создает клавиатуру с кнопкой для открытия веб-приложения"""
    keyboard = InlineKeyboardMarkup()
    webapp_btn = InlineKeyboardButton(
        text='🏪 Открыть магазин', 
        web_app=types.WebAppInfo(url=WEBAPP_URL)
    )
    keyboard.add(webapp_btn)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с кнопкой для запуска веб-приложения
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_btn = types.KeyboardButton(
        text="🛍 Открыть магазин", 
        web_app=types.WebAppInfo(url=f"https://t.me/six_o_clock_test_bot/{BOT_WEBAPP_NAME}")
    )
    keyboard.add(webapp_btn)
    
    # Добавляем инлайн кнопки
    inline_keyboard = types.InlineKeyboardMarkup()
    info_btn = types.InlineKeyboardButton("ℹ️ О нас", callback_data="about")
    support_btn = types.InlineKeyboardButton("🆘 Поддержка", callback_data="support")
    inline_keyboard.add(info_btn, support_btn)
    
    welcome_text = (
        "👋 Добро пожаловать в наш магазин!\n\n"
        "🛍 Нажмите кнопку «Открыть магазин» чтобы начать покупки\n\n"
        "ℹ️ Используйте меню ниже, чтобы:\n"
        "• Узнать больше о нас\n"
        "• Связаться с поддержкой"
    )
    
    bot.send_message(
        message.chat.id, 
        welcome_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    bot.send_message(
        message.chat.id,
        "Выберите действие:",
        reply_markup=inline_keyboard
    )

@bot.message_handler(commands=['shop'])
def open_shop(message):
    """Обработчик команды /shop"""
    bot.send_message(
        message.chat.id,
        "🏪 Добро пожаловать в наш магазин!\nВыберите товары:",
        reply_markup=get_webapp_keyboard()
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработчик команды /help"""
    help_text = (
        "📌 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/shop - Открыть магазин\n"
        "/help - Показать это сообщение\n"
        "/info - Информация о магазине\n"
        "/support - Связаться с поддержкой\n\n"
        "По всем вопросам обращайтесь в поддержку!"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['info'])
def send_info(message):
    """Обработчик команды /info"""
    info_text = (
        "ℹ️ О магазине 6 O'clock Shop:\n\n"
        "🏪 Мы предлагаем широкий ассортимент товаров:\n"
        "   • Мужская одежда\n"
        "   • Женская одежда\n"
        "   • Аксессуары\n\n"
        "🚚 Доставка по всей России\n"
        "💳 Удобные способы оплаты\n"
        "👍 Гарантия качества\n\n"
        "📞 Контакты:\n"
        f"   • Телефон: {TG_SUPPORT_PHONE}\n"
        f"   • Email: {TG_SUPPORT_EMAIL}\n"
        f"   • Время работы: {TG_SUPPORT_WORK_TIME}\n\n"
        
    )
    bot.send_message(message.chat.id, info_text)

@bot.message_handler(commands=['support'])
def send_support(message):
    """Обработчик команды /support"""
    support_text = (
        "🆘 Служба поддержки\n\n"
        "Если у вас возникли вопросы или проблемы, вы можете:\n\n"
        f"1️⃣ Написать нам на почту: {TG_SUPPORT_EMAIL}\n"
        f"2️⃣ Позвонить по телефону: {TG_SUPPORT_PHONE}\n"
        "3️⃣ Оставить сообщение прямо здесь\n\n"
        f"⏱ Время работы поддержки: {TG_SUPPORT_WORK_TIME}\n"
        "⚡️ Среднее время ответа: 15 минут"
    )
    
    # Создаем инлайн-кнопку для связи с поддержкой
    keyboard = InlineKeyboardMarkup()
    support_btn = InlineKeyboardButton(
        text='📝 Написать в поддержку',
        url=f'https://t.me/{TG_SUPPORT_USERNAME}'  # Замените на username поддержки
    )
    keyboard.add(support_btn)
    
    bot.send_message(
        message.chat.id,
        support_text,
        reply_markup=keyboard
    )

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Обработчик получения контакта пользователя"""
    if message.contact is not None:
        contact_info = (
            f"✅ Спасибо! Ваш контакт сохранен:\n\n"
            f"📱 Телефон: {message.contact.phone_number}\n"
            f"👤 Имя: {message.contact.first_name}"
        )
        bot.send_message(
            message.chat.id,
            contact_info,
            reply_markup=get_main_keyboard()
        )
        # Здесь можно добавить сохранение контакта в базу данных

@bot.message_handler(func=lambda message: message.text == '🛍 Магазин')
def handle_shop_button(message):
    """Обработчик нажатия кнопки 'Магазин'"""
    open_shop(message)

@bot.message_handler(func=lambda message: message.text == 'ℹ️ Информация')
def handle_info_button(message):
    """Обработчик нажатия кнопки 'Информация'"""
    send_info(message)

@bot.message_handler(func=lambda message: message.text == '🆘 Поддержка')
def handle_support_button(message):
    """Обработчик нажатия кнопки 'Поддержка'"""
    send_support(message)

# Обработчик для веб-приложения
@bot.message_handler(content_types=['web_app_data'])
def web_app_handler(message):
    """Обработчик данных от веб-приложения"""
    try:
        data = json.loads(message.web_app_data.data)
        # Обработка данных от веб-приложения
        bot.send_message(
            message.chat.id,
            f"✅ Данные получены:\n{json.dumps(data, indent=2, ensure_ascii=False)}"
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка обработки данных: {str(e)}"
        )

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()

