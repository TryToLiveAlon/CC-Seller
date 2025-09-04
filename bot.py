from pyrogram import Client
import config
import handlers  # this will auto-import all handlers

app = Client(
    "gamebot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

print("🤖 Bot is running...")
app.run()
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)
        user_db.update_balance(user_id, amount)
        await message.reply_text(f"✅ Added {amount} {config.CURRENCY} to {user_id}")
    except:
        await message.reply_text("Usage: /addbalance <user_id> <amount>")


print("🤖 Bot is running with Pyrogram...")
app.run()

