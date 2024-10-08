# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from models import get_user, update_balance
import logging
import asyncio

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
TOKEN = '7917233968:AAHbWqKEMPfcxLGuuHyqRTKtlAEKHhr3d5M'

# Start command handler
def start(update: Update, context: CallbackContext):
    
    user = update.effective_user
    get_user(user.id, user.username)
    
    keyboard = [
        [InlineKeyboardButton("🎰 Roulette", callback_data='roulette')],
        [InlineKeyboardButton("♠️ Poker", callback_data='poker')],
        [InlineKeyboardButton("🃏 Blackjack", callback_data='blackjack')],
        [InlineKeyboardButton("💰 Balance", callback_data='balance')],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data='leaderboard')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"Welcome to the Casino, {user.first_name}!\nChoose a game to play:"
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Command to stop the bot
async def stop(update, context):
    # Retrieve the application from the context
    application = context.application
    print("Stop function")
    await update.message.reply_text("Bot is shutting down...")

    # Stop the application
    await application.stop()

# Callback query handler
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = query.from_user
    data = query.data
    
    if data == 'balance':
        user_data = get_user(user.id, user.username)
        query.edit_message_text(text=f"💰 Your balance: {user_data.balance:.2f} 💰")
    
    elif data == 'leaderboard':
        leaderboard = get_leaderboard()
        message = "🏆 **Leaderboard** 🏆\n\n"
        for idx, (username, balance) in enumerate(leaderboard, start=1):
            message += f"{idx}. {username} - {balance:.2f}\n"
        query.edit_message_text(text=message, parse_mode='Markdown')
    
    elif data in ['roulette', 'poker', 'blackjack']:
        # Redirect to the respective game
        if data == 'roulette':
            start_roulette(query, context)
        elif data == 'poker':
            start_poker(query, context)
        elif data == 'blackjack':
            start_blackjack(query, context)

# Function to get the leaderboard
def get_leaderboard():
    users = session.query(User).order_by(User.balance.desc()).limit(10).all()
    return [(user.username or "Anonymous", user.balance) for user in users]

# Placeholder functions for games
def start_roulette(query, context):
    query.edit_message_text(text="🎰 **Roulette** is under construction! Stay tuned.")

def start_poker(query, context):
    query.edit_message_text(text="♠️ **Poker** is under construction! Stay tuned.")

def start_blackjack(query, context):
    query.edit_message_text(text="🃏 **Blackjack** is under construction! Stay tuned.")

# bot.py (continued)

import random

def start_roulette(query, context):
    keyboard = [
        [InlineKeyboardButton("Place a Bet", callback_data='roulette_bet')],
        [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="🎰 **Roulette**\nChoose an option:", parse_mode='Markdown', reply_markup=reply_markup)

def roulette_bet(query, context):
    keyboard = [
        [InlineKeyboardButton("Red", callback_data='roulette_bet_red'),
         InlineKeyboardButton("Black", callback_data='roulette_bet_black')],
        [InlineKeyboardButton("Odd", callback_data='roulette_bet_odd'),
         InlineKeyboardButton("Even", callback_data='roulette_bet_even')],
        [InlineKeyboardButton("Number", callback_data='roulette_bet_number')],
        [InlineKeyboardButton("Back to Games", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="💰 **Place your bet**\nChoose a bet type:", parse_mode='Markdown', reply_markup=reply_markup)

def roulette_place_bet_number(query, context):
    query.edit_message_text(text="🔢 Enter a number between 0 and 36:")

    return # Here, you need to set up a handler to capture the user's input.

# Modify the button handler to manage Roulette bets
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = query.from_user
    data = query.data
    
    if data == 'balance':
        user_data = get_user(user.id, user.username)
        query.edit_message_text(text=f"💰 Your balance: {user_data.balance:.2f} 💰")
    
    elif data == 'leaderboard':
        leaderboard = get_leaderboard()
        message = "🏆 **Leaderboard** 🏆\n\n"
        for idx, (username, balance) in enumerate(leaderboard, start=1):
            message += f"{idx}. {username} - {balance:.2f}\n"
        query.edit_message_text(text=message, parse_mode='Markdown')
    
    elif data == 'back_to_menu':
        start(update, context)
    
    elif data == 'roulette':
        start_roulette(query, context)
    
    elif data == 'roulette_bet':
        roulette_bet(query, context)
    
    elif data.startswith('roulette_bet_'):
        bet_type = data.replace('roulette_bet_', '')
        handle_roulette_bet(query, context, bet_type)
    
    elif data in ['poker', 'blackjack']:
        # Handle other games similarly
        if data == 'poker':
            start_poker(query, context)
        elif data == 'blackjack':
            start_blackjack(query, context)

def handle_roulette_bet(query, context, bet_type):
    user = query.from_user
    user_data = get_user(user.id, user.username)
    
    if bet_type in ['red', 'black', 'odd', 'even']:
        # Prompt user to enter bet amount
        context.user_data['roulette_bet_type'] = bet_type
        query.edit_message_text(text=f"💰 **{bet_type.capitalize()}**\nEnter your bet amount:")
    
    elif bet_type == 'number':
        # Prompt user to enter a specific number
        context.user_data['roulette_bet_type'] = bet_type
        query.edit_message_text(text="🔢 Enter a number between 0 and 36:")
    
    # Register a message handler to capture the bet amount or number
    # This requires adding a handler that listens to the next message from the user

def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    text = update.message.text
    if 'roulette_bet_type' in context.user_data:
        bet_type = context.user_data['roulette_bet_type']
        try:
            bet_amount = float(text)
        except ValueError:
            update.message.reply_text("❌ Please enter a valid number for the bet amount.")
            return
        
        user_data = get_user(user.id, user.username)
        if bet_amount > user_data.balance:
            update.message.reply_text("❌ You don't have enough balance for that bet.")
            return
        
        if bet_type == 'number':
            try:
                bet_number = int(text)
                if not 0 <= bet_number <= 36:
                    update.message.reply_text("❌ Please enter a number between 0 and 36.")
                    return
            except ValueError:
                update.message.reply_text("❌ Please enter a valid number between 0 and 36.")
                return
            context.user_data['roulette_bet_number'] = bet_number
        
        # Proceed to spin the roulette
        outcome = spin_roulette()
        update.message.reply_text(f"🎡 Roulette spun: **{outcome['number']} {outcome['color']}**", parse_mode='Markdown')
        
        # Determine if user won
        won = False
        payout = 0
        if bet_type == 'red' and outcome['color'] == 'red':
            won = True
            payout = bet_amount * 2
        elif bet_type == 'black' and outcome['color'] == 'black':
            won = True
            payout = bet_amount * 2
        elif bet_type == 'odd' and outcome['number'] != 0 and outcome['number'] % 2 == 1:
            won = True
            payout = bet_amount * 2
        elif bet_type == 'even' and outcome['number'] != 0 and outcome['number'] % 2 == 0:
            won = True
            payout = bet_amount * 2
        elif bet_type == 'number' and outcome['number'] == context.user_data.get('roulette_bet_number'):
            won = True
            payout = bet_amount * 35
        
        if won:
            update_balance(user.id, payout)
            update.message.reply_text(f"🎉 You won! Your new balance is **{user_data.balance + payout:.2f}**", parse_mode='Markdown')
        else:
            update_balance(user.id, -bet_amount)
            update.message.reply_text(f"😞 You lost. Your new balance is **{user_data.balance - bet_amount:.2f}**", parse_mode='Markdown')
        
        # Clear user data
        context.user_data.pop('roulette_bet_type', None)
        context.user_data.pop('roulette_bet_number', None)

def spin_roulette():
    number = random.randint(0, 36)
    if number == 0:
        color = 'green'
    elif number % 2 == 0:
        color = 'black'
    else:
        color = 'red'
    return {'number': number, 'color': color}

async def main():
    # Create the Application and pass your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))  # Stop command handler
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    chat_id = "756357081"  # Replace with your chat ID
    #await application.bot.send_message(chat_id=chat_id, text="Bot is starting!")
    
    await application.initialize()
    await application.run_polling()

# Check if there's already an event loop running
if __name__ == '__main__':
    # Try to run the bot using asyncio.run()
    asyncio.run(main())