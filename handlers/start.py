from pyrogram import filters
from bot import app
import config
from DB.user import user_db

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_db.add_user(message.from_user.id, message.from_user.username or "Unknown")
    await message.reply_text(
        f"{config.WELCOME_MESSAGE}\n\nYour balance: 0 {config.CURRENCY}"
    )
