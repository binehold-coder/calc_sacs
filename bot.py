"""
Telegram Bot - Calculateur de Sacs de Palettes (Sacs Calculator)
Version: 1.0
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

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for ConversationHandler
LINES, BAGS = range(2)

# Constants
MIN_LINES = 1
MAX_LINES = 17
MIN_BAGS = 1
MAX_BAGS = 10


class SacsCalculator:
    """Class for calculating number of bags"""
    
    @staticmethod
    def calculate(lines: int, bags: int) -> int:
        """
        Calculates total number of bags
        
        Logic:
        - Odd lines (1,3,5...): 10 bags
        - Even lines (2,4,6...): 9 bags
        - Then add remaining bags
        """
        if lines < MIN_LINES or lines > MAX_LINES or bags < MIN_BAGS or bags > MAX_BAGS:
            return None
        
        # Number of full odd and even lines
        odd_lines = (lines + 1) // 2  # 1,3,5,7,9,11,13,15,17
        even_lines = lines // 2       # 2,4,6,8,10,12,14,16
        
        # Calculate bags
        bags_from_lines = (odd_lines * 10) + (even_lines * 9)
        total_bags = bags_from_lines + bags
        
        return total_bags
    
    @staticmethod
    def is_valid_lines(value: str) -> bool:
        """Validates if lines input is valid (1-17)"""
        try:
            num = int(value)
            return MIN_LINES <= num <= MAX_LINES
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_bags(value: str) -> bool:
        """Validates if bags input is valid (1-10)"""
        try:
            num = int(value)
            return MIN_BAGS <= num <= MAX_BAGS
        except ValueError:
            return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for /start command"""
    welcome_text = (
        "🤖 Bienvenue dans le Calculateur de Sacs de Palettes !\n\n"
        "Je vais vous aider à calculer le nombre total de sacs.\n\n"
        "Logique de calcul :\n"
        "• Lignes impaires (1,3,5...) : 10 sacs\n"
        "• Lignes paires (2,4,6...) : 9 sacs\n\n"
        "Valeurs autorisées : 1-17\n\n"
        "Commençons ! Entrez le nombre de lignes :"
    )
    
    await update.message.reply_text(welcome_text)
    return LINES


async def get_lines(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get number of lines"""
    user_input = update.message.text.strip()
    
    if not SacsCalculator.is_valid_lines(user_input):
        error_text = (
            "❌ Erreur ! Veuillez entrer un nombre entre 1 et 17.\n"
            "Essayez encore :"
        )
        await update.message.reply_text(error_text)
        return LINES
    
    # Save number of lines
    context.user_data['lines'] = int(user_input)
    
    text = f"✅ Lignes : {user_input}\n\nMaintenant, entrez le nombre de sacs supplémentaires (1-10) :"
    await update.message.reply_text(text)
    return BAGS


async def get_bags(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get number of bags and calculate result"""
    user_input = update.message.text.strip()
    
    if not SacsCalculator.is_valid_bags(user_input):
        error_text = (
            "❌ Erreur ! Veuillez entrer un nombre entre 1 et 10.\n"
            "Essayez encore :"
        )
        await update.message.reply_text(error_text)
        return BAGS
    
    bags = int(user_input)
    lines = context.user_data['lines']
    
    # Calculate result
    total = SacsCalculator.calculate(lines, bags)
    
    # Detailed calculation for user
    odd_lines = (lines + 1) // 2
    even_lines = lines // 2
    bags_from_lines = (odd_lines * 10) + (even_lines * 9)
    
    result_text = (
        f"📊 RÉSULTAT DU CALCUL\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Lignes : {lines}\n"
        f"Sacs supplémentaires : {bags}\n\n"
        f"📐 Détails :\n"
        f"• Lignes impaires : {odd_lines} × 10 = {odd_lines * 10} sacs\n"
        f"• Lignes paires : {even_lines} × 9 = {even_lines * 9} sacs\n"
        f"• Sacs supplémentaires : {bags}\n\n"
        f"✅ TOTAL : {total} sacs\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Tapez /calc pour un nouveau calcul ou /help pour l'aide"
    )
    
    await update.message.reply_text(result_text)
    
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /help command"""
    help_text = (
        "📖 AIDE DU BOT\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 Commandes disponibles :\n"
        "/start - Commencer un nouveau calcul\n"
        "/calc - Calculer le nombre de sacs\n"
        "/help - Afficher cette aide\n\n"
        "📐 Logique de calcul :\n"
        "• Lignes impaires (1,3,5,...,17) : 10 sacs chacune\n"
        "• Lignes paires (2,4,6,...,16) : 9 sacs chacune\n"
        "• Ensuite, les sacs supplémentaires sont ajoutés\n\n"
        "Exemple :\n"
        "11 lignes + 8 sacs =\n"
        "(6×10 + 5×9) + 8 = 60 + 45 + 8 = 113 sacs\n\n"
        "✅ Valeurs autorisées : 1-17\n"
        "❌ Toutes les autres valeurs seront rejetées"
    )
    await update.message.reply_text(help_text)


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for /calc command for new calculation"""
    text = "Entrez le nombre de lignes (1-17) :"
    await update.message.reply_text(text)
    return LINES


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel calculation"""
    await update.message.reply_text(
        "❌ Calcul annulé.\nTapez /calc pour un nouveau calcul."
    )
    return ConversationHandler.END


def main():
    """Main function to start the bot"""
    # Get token from environment variables
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("❌ Erreur: TELEGRAM_BOT_TOKEN introuvable dans le fichier .env!")
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Conversation handler for calculations
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
    
    # Add handlers
    application.add_handler(calc_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # Start bot
    logger.info("🚀 Bot démarré! En attente de messages...")
    application.run_polling()


if __name__ == '__main__':
    main()
