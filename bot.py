from pyrogram import Client, filters
import config
from DB.user import user_db

# Create bot instance
app = Client(
    "gamebot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)


# --- /start ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_db.add_user(message.from_user.id, message.from_user.username or "Unknown")
    await message.reply_text(
        f"{config.WELCOME_MESSAGE}\n\nYour balance: 0 {config.CURRENCY}"
    )


# --- /balance ---
@app.on_message(filters.command("balance") & filters.private)
async def balance_cmd(client, message):
    user = user_db.get_user(message.from_user.id)
    if user:
        await message.reply_text(f"💰 Balance: {user['balance']} {config.CURRENCY}")
    else:
        await message.reply_text("⚠️ You are not registered yet! Use /start")


# --- /addbalance <id> <amount> (Admin Only) ---
@app.on_message(filters.command("addbalance") & filters.user(config.ADMIN_IDS))
async def add_balance_cmd(client, message):
    try:
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)
        user_db.update_balance(user_id, amount)
        await message.reply_text(f"✅ Added {amount} {config.CURRENCY} to {user_id}")
    except:
        await message.reply_text("Usage: /addbalance <user_id> <amount>")


print("🤖 Bot is running with Pyrogram...")
app.run()

