import os
import logging
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
WEBAPP_URL = os.getenv('TG_WEB_APP_URL')
SUPPORT_USERNAME = os.getenv('TG_SUPPORT_USERNAME', 'support').lstrip('@')

# Проверка переменных окружения
if not all([BOT_TOKEN, WEBAPP_URL, SUPPORT_USERNAME]):
    missing = []
    if not BOT_TOKEN: missing.append('TG_BOT_TOKEN')
    if not WEBAPP_URL: missing.append('TG_WEB_APP_URL')
    if not SUPPORT_USERNAME: missing.append('TG_SUPPORT_USERNAME')
    raise ValueError(f"Отсутствуют обязательные переменные окружения: {', '.join(missing)}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Минимальный обработчик ошибок."""
    logger.error(f"Ошибка: {context.error}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start с красивым меню."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="🛍 Открыть магазин",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        
        [
            InlineKeyboardButton(text="ℹ️ О магазине", callback_data="about"),
            InlineKeyboardButton(text="👨‍💻 Поддержка", url=f"https://t.me/{SUPPORT_USERNAME}")
        ]
    ])
    
    await update.message.reply_text(
        '👋 *Добро пожаловать в 6 O\'clock Shop!*\n\n'
        '🔸 Стильная одежда\n'
        '🔸 Качественные аксессуары\n'
        '🔸 Доставка по всей России\n\n'
        'Выберите действие:',
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Красивая информация о магазине."""
    await update.callback_query.answer()
    
    about_text = (
        "🏪 *6 O'clock Shop*\n\n"
        "Мы предлагаем широкий ассортимент товаров:\n"
        "• Качественная одежда от лучших брендов\n"
        "• Стильные аксессуары для любого образа\n"
        "• Уникальные коллекции с доставкой по России\n\n"
        "🕒 *Время работы:* Круглосуточно\n"
        "🚚 *Доставка:* По всей России\n"
        "💳 *Оплата:* Карты, СБП, наличные при получении"
    )
    
    back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")]
    ])
    
    await update.callback_query.message.edit_text(
        about_text,
        reply_markup=back_keyboard,
        parse_mode='Markdown'
    )

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Каталог товаров."""
    await update.callback_query.answer()
    
    catalog_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👕 Одежда", web_app=WebAppInfo(url=f"{WEBAPP_URL}/category/clothes"))],
        [InlineKeyboardButton("👟 Обувь", web_app=WebAppInfo(url=f"{WEBAPP_URL}/category/shoes"))],
        [InlineKeyboardButton("🧢 Аксессуары", web_app=WebAppInfo(url=f"{WEBAPP_URL}/category/accessories"))],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ])
    
    await update.callback_query.message.edit_text(
        "📋 *Каталог товаров*\n\n"
        "Выберите категорию:",
        reply_markup=catalog_keyboard,
        parse_mode='Markdown'
    )

async def new_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Новинки."""
    await update.callback_query.answer()
    
    new_items_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Посмотреть новинки", web_app=WebAppInfo(url=f"{WEBAPP_URL}/new"))],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ])
    
    await update.callback_query.message.edit_text(
        "✨ *Новинки этой недели*\n\n"
        "Мы постоянно обновляем ассортимент!\n"
        "Нажмите кнопку ниже, чтобы увидеть последние поступления:",
        reply_markup=new_items_keyboard,
        parse_mode='Markdown'
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню."""
    await update.callback_query.answer()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="🛍 Открыть магазин",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [
            InlineKeyboardButton(text="👕 Каталог", callback_data="catalog"),
            InlineKeyboardButton(text="🔥 Новинки", callback_data="new_items")
        ],
        [
            InlineKeyboardButton(text="ℹ️ О магазине", callback_data="about"),
            InlineKeyboardButton(text="👨‍💻 Поддержка", url=f"https://t.me/{SUPPORT_USERNAME}")
        ]
    ])
    
    await update.callback_query.message.edit_text(
        '👋 *Добро пожаловать в 6 O\'clock Shop!*\n\n'
        '🔸 Стильная одежда\n'
        '🔸 Качественные аксессуары\n'
        '🔸 Доставка по всей России\n\n'
        'Выберите действие:',
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

def run_bot():
    """Запуск бота."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(about, pattern="^about$"))
    application.add_handler(CallbackQueryHandler(catalog, pattern="^catalog$"))
    application.add_handler(CallbackQueryHandler(new_items, pattern="^new_items$"))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"))
    application.add_error_handler(error_handler)

    print("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)



