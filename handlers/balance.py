from pyrogram import filters
from bot import app
import config
from DB.user import user_db

@app.on_message(filters.command("balance") & filters.private)
async def balance_cmd(client, message):
    user = user_db.get_user(message.from_user.id)
    if user:
        await message.reply_text(f"💰 Balance: {user['balance']} {config.CURRENCY}")
    else:
        await message.reply_text("⚠️ You are not registered yet! Use /start")
      
