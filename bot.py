"""
Telegram Bot Калькулятор мешков поддонов (Sacs Calculator)
Версия: 1.0
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
LINES, BAGS = range(2)

# Константы
MIN_VALUE = 1
MAX_VALUE = 17


class SacsCalculator:
    """Класс для расчёта количества мешков"""
    
    @staticmethod
    def calculate(lines: int, bags: int) -> int:
        """
        Расчитывает общее количество мешков
        
        Логика:
        - Нечётные линии (1,3,5...): 10 мешков
        - Чётные линии (2,4,6...): 9 мешков
        - Затем добавляем остаток мешков
        """
        if lines < 1 or lines > 17 or bags < 1 or bags > 17:
            return None
        
        # Количество полных чётных и нечётных линий
        odd_lines = (lines + 1) // 2  # 1,3,5,7,9,11,13,15,17
        even_lines = lines // 2       # 2,4,6,8,10,12,14,16
        
        # Расчитываем мешки
        bags_from_lines = (odd_lines * 10) + (even_lines * 9)
        total_bags = bags_from_lines + bags
        
        return total_bags
    
    @staticmethod
    def is_valid_input(value: str) -> bool:
        """Проверяет, является ли входное значение валидным"""
        try:
            num = int(value)
            return MIN_VALUE <= num <= MAX_VALUE
        except ValueError:
            return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /start"""
    welcome_text = (
        "🤖 Добро пожаловать в Калькулятор Мешков Поддонов!\n\n"
        "Я помогу тебе расчитать общее количество мешков.\n\n"
        "Логика расчёта:\n"
        "• Нечётные линии (1,3,5...): 10 мешков\n"
        "• Чётные линии (2,4,6...): 9 мешков\n\n"
        "Допустимые значения: 1-17\n\n"
        "Давай начнём! Введи количество линий (Lignes):"
    )
    
    await update.message.reply_text(welcome_text)
    return LINES


async def get_lines(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получение количества линий"""
    user_input = update.message.text.strip()
    
    if not SacsCalculator.is_valid_input(user_input):
        error_text = (
            "❌ Ошибка! Пожалуйста, введи число от 1 до 17.\n"
            "Попробуй ещё раз:"
        )
        await update.message.reply_text(error_text)
        return LINES
    
    # Сохраняем количество линий
    context.user_data['lines'] = int(user_input)
    
    text = f"✅ Линии: {user_input}\n\nТеперь введи количество мешков (Sacs):"
    await update.message.reply_text(text)
    return BAGS


async def get_bags(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получение количества мешков и расчёт результата"""
    user_input = update.message.text.strip()
    
    if not SacsCalculator.is_valid_input(user_input):
        error_text = (
            "❌ Ошибка! Пожалуйста, введи число от 1 до 17.\n"
            "Попробуй ещё раз:"
        )
        await update.message.reply_text(error_text)
        return BAGS
    
    bags = int(user_input)
    lines = context.user_data['lines']
    
    # Расчитываем результат
    total = SacsCalculator.calculate(lines, bags)
    
    # Детальный расчёт для пользователя
    odd_lines = (lines + 1) // 2
    even_lines = lines // 2
    bags_from_lines = (odd_lines * 10) + (even_lines * 9)
    
    result_text = (
        f"📊 РЕЗУЛЬТАТ РАСЧЁТА\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Lignes: {lines}\n"
        f"Sacs supplémentaires: {bags}\n\n"
        f"📐 Детализация:\n"
        f"• Нечётные линии: {odd_lines} × 10 = {odd_lines * 10} мешков\n"
        f"• Чётные линии: {even_lines} × 9 = {even_lines * 9} мешков\n"
        f"• Дополнительные мешки: {bags}\n\n"
        f"✅ ИТОГО: {total} мешков\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Введи /calc для нового расчёта или /help для справки"
    )
    
    await update.message.reply_text(result_text)
    
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = (
        "📖 СПРАВКА ПО БОТУ\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 Доступные команды:\n"
        "/start - Начать новый расчёт\n"
        "/calc - Расчитать количество мешков\n"
        "/help - Показать эту справку\n\n"
        "📐 Логика расчёта:\n"
        "• Нечётные линии (1,3,5,...,17): 10 мешков каждая\n"
        "• Чётные линии (2,4,6,...,16): 9 мешков каждая\n"
        "• Затем добавляются дополнительные мешки\n\n"
        "Пример:\n"
        "11 линий + 8 мешков =\n"
        "(6×10 + 5×9) + 8 = 60 + 45 + 8 = 113 мешков\n\n"
        "✅ Допустимые значения: 1-17\n"
        "❌ Любые другие значения будут отклонены"
    )
    await update.message.reply_text(help_text)


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /calc для нового расчёта"""
    text = "Введи количество линий (Lignes) от 1 до 17:"
    await update.message.reply_text(text)
    return LINES


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена расчёта"""
    await update.message.reply_text(
        "❌ Расчёт отменён.\nВведи /calc для нового расчёта."
    )
    return ConversationHandler.END


def main():
    """Основная функция запуска бота"""
    # Получаем токен из переменных окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден в .env файле!")
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    
    # Создаём приложение
    application = Application.builder().token(token).build()
    
    # Обработчик конверсации для расчётов
    calc_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('calc', calc_command)
        ],
        states={
            LINES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_lines)],
            BAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bags)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Добавляем обработчики
    application.add_handler(calc_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # Запускаем бота
    logger.info("🚀 Бот запущен! Ожидание сообщений...")
    application.run_polling()


if __name__ == '__main__':
    main()
