import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters

TOKEN = "7917233968:AAHbWqKEMPfcxLGuuHyqRTKtlAEKHhr3d5M"  # Replace with your bot token from BotFather

# Start command handler
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(f"Welcome {user.first_name}, you can play games like poker, blackjack, and roulette here.")

# Stop command handler
async def stop(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot is shutting down...")
    await context.application.stop()

# Button callback handler (placeholder for your actual game handling logic)
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="This is a placeholder for button interactions.")

# Message handler (handle regular text messages)
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

# Main function to run the bot
async def main():
    # Create the Application and pass your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling for updates
    await application.run_polling()

# Entry point for the script
if __name__ == '__main__':
    try:
        # Attempt to run the bot using asyncio.run()
        asyncio.run(main())
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            # If an event loop is already running, use the existing loop
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
