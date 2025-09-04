from pyrogram import filters
from bot import app
import config
from DB.user import user_db

# --- /userinfo <id> ---
@app.on_message(filters.command("userinfo") & filters.user(config.ADMIN_IDS))
async def user_info_cmd(client, message):
    try:
        _, uid = message.text.split()
        uid = int(uid)
        user = user_db.get_user(uid)
        if user:
            await message.reply_text(
                f"👤 User ID: {user['user_id']}\n"
                f"📛 Username: {user['username']}\n"
                f"💰 Balance: {user['balance']} {config.CURRENCY}\n"
                f"🔑 Hash: <code>{user['hash']}</code>\n"
                f"📅 Created: {user['created_at']}"
            )
        else:
            await message.reply_text("❌ User not found.")
    except:
        await message.reply_text("Usage: /userinfo <user_id>")


# --- /addbalance <id> <amount> ---
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
      
