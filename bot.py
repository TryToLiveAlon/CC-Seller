#!/usr/bin/env python3
import telebot
from telebot import types
import json
import os
import requests
from datetime import datetime
from config import (
    API_TOKEN, CHANNEL_1, CHANNEL_2,
    REFS_FOR_COOKIE, COOKIE_REWARD_AMOUNT,
    DATA_FILE, ADMIN_IDS, WELCOME_MEDIA_URL,
    XROCKET_API_KEY, XROCKET_API_URL
)

bot = telebot.TeleBot(API_TOKEN)

# ---------- temporary state (lost on restart) ----------
pending_actions = {}

# ---------- storage helpers ----------
def load_db():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def get_user(user_id):
    db = load_db()
    return db.get(str(user_id))

def register_user(user_obj, ref_by=None):
    db = load_db()
    uid = str(user_obj.id)
    if uid not in db:
        db[uid] = {
            "id": user_obj.id,
            "username": user_obj.username,
            "first_name": user_obj.first_name,
            "balance": 0.0,
            "register_at": datetime.utcnow().isoformat(),
            "ref_by": ref_by,
            "referrals": [],
            "cookies": 0,
            "purchases": [],
        }
    else:
        db[uid]["username"] = user_obj.username
        db[uid]["first_name"] = user_obj.first_name
    save_db(db)
    return db[uid]

def add_referral(referrer_id, new_user_id):
    db = load_db()
    rid, nid = str(referrer_id), str(new_user_id)
    if rid == nid or rid not in db:
        return False
    if nid in db[rid]["referrals"]:
        return False
    db[rid]["referrals"].append(nid)
    refs = len(db[rid]["referrals"])
    rewarded = False
    if refs % REFS_FOR_COOKIE == 0:
        db[rid]["cookies"] += 1
        db[rid]["balance"] += COOKIE_REWARD_AMOUNT
        rewarded = True
    save_db(db)
    return rewarded

# ---------- keyboards ----------
def join_message_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{CHANNEL_1.lstrip('@')}"))
    kb.add(types.InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{CHANNEL_2.lstrip('@')}"))
    kb.add(types.InlineKeyboardButton("✅ Verify Join & Go to Personal Area", callback_data="verify_join"))
    return kb

def personal_area_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("➕ Top Up Balance", callback_data="topup"))
    kb.add(types.InlineKeyboardButton("💸 Send money to another user", callback_data="send_money"))
    kb.add(types.InlineKeyboardButton("📜 Balance History", callback_data="history"))
    kb.add(types.InlineKeyboardButton("🔙 Back to Home", callback_data="back_home"))  # 👈 new
    return kb

    
def home_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        types.InlineKeyboardButton("👤 Personal Area", callback_data="personal_area"),
        types.InlineKeyboardButton("🛒 Purchase", callback_data="purchase")
    )
    kb.add(types.InlineKeyboardButton("CC",callback_data="cc"))
    kb.add(types.InlineKeyboardButton("BIN",callback_data="bin"))
    kb.row(
        types.InlineKeyboardButton("✉️ Gmail", callback_data="gmail"),
        types.InlineKeyboardButton("📷 RDP", callback_data="rdp")
    )
    kb.row(
        types.InlineKeyboardButton("🔃 Method", callback_data="methods"),
        types.InlineKeyboardButton("Enroll", callback_data="enroll")
    )
    kb.row(
        types.InlineKeyboardButton("🆘 Support", url="https://t.me/your_support"),
        types.InlineKeyboardButton("⚠️ Rules", callback_data="rules")
    )
    kb.add(types.InlineKeyboardButton("❔ Other",callback_data="other"))
    return kb
    
# ---------- handlers ----------
@bot.message_handler(commands=['start'])
def handle_start(message):
    arg = None
    if "start=" in message.text:
        arg = message.text.split("start=")[-1].strip()
    elif len(message.text.split()) > 1:
        arg = message.text.split()[1].strip()

    ref_by = int(arg) if arg and arg.isdigit() else None
    user = register_user(message.from_user, ref_by)
    if ref_by:
        try:
            rewarded = add_referral(ref_by, message.from_user.id)
            if rewarded:
                bot.send_message(ref_by, f"🎉 Referral milestone reached! +{COOKIE_REWARD_AMOUNT} balance.")
        except Exception:
            pass

    text = (
        f"🚨 Mandatory Step 🚨\n\n"
        f"Dear {message.from_user.first_name},\n"
        "To continue using this bot, please join our official channels."
    )
    markup = join_message_keyboard()
    try:
        if WELCOME_MEDIA_URL:
            if WELCOME_MEDIA_URL.endswith((".mp4", ".mov", ".avi", ".mkv")):
                bot.send_video(message.chat.id, WELCOME_MEDIA_URL, caption=text, reply_markup=markup)
            else:
                bot.send_photo(message.chat.id, WELCOME_MEDIA_URL, caption=text, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def handle_callbacks(call):
    user_id, data = call.from_user.id, call.data
    chat_id, msg_id = call.message.chat.id, call.message.message_id

    if data == "verify_join":
        ok1 = ok2 = False
        try:
            mem1 = bot.get_chat_member(CHANNEL_1, user_id)
            ok1 = mem1.status not in ("left", "kicked")
        except: pass
        try:
            mem2 = bot.get_chat_member(CHANNEL_2, user_id)
            ok2 = mem2.status not in ("left", "kicked")
        except: pass

        if ok1 and ok2:
           bot.answer_callback_query(call.id, "✅ Verified!")
           bot.delete_message(chat_id, msg_id)
           bot.send_message(
           chat_id,
           "🎉 You have successfully joined!\n\nWelcome to the main menu 👇",
           reply_markup=home_keyboard())

        else:
            bot.answer_callback_query(call.id, "❌ Not joined yet.")
            bot.delete_message(chat_id, msg_id)
            bot.send_message(chat_id, "⚠️ You must join both channels.", reply_markup=join_message_keyboard())

    elif data == "personal_area":
        u = get_user(user_id)
        text = (
            "➖➖➖➖➖➖➖➖➖➖\n"
            f"👨🏻‍💻 Your ID {user_id}\n"
            f"💰 Balance {u['balance']:.2f}\n"
            f"🕘 Register at {u['register_at'][:10]}\n\n"
            f"Ref link https://t.me/{bot.get_me().username}?start={user_id}\n"
            f"Number of referrals {len(u['referrals'])}\n"
            "➖➖➖➖➖➖➖➖➖➖"
        )
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, text, reply_markup=personal_area_keyboard(), disable_web_page_preview=True)

    elif data == "topup":
        pending_actions[user_id] = {"action": "topup_amount"}
        bot.delete_message(chat_id, msg_id)
        bot.send_message(
            chat_id,
            "💳 Please enter the amount you want to top up (USD):",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🔙 Cancel", callback_data="personal_area")
            )
        )

    elif data == "history":
        u = get_user(user_id)
        hist = u.get("purchases", [])
        txt = "📜 History:\n" + ("\n".join(hist) if hist else "No history yet.")
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, txt, reply_markup=personal_area_keyboard())

    elif data == "send_money":
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, "💸 Send money flow (to be implemented).", reply_markup=personal_area_keyboard())

    elif data == "rules":
        bot.send_message(user_id, "⚠️ Rules:\n1) No spam\n2) Respect others")

    elif data == "back_home":
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, "🏠 Back to Home Menu:", reply_markup=home_keyboard())
    

# ---------- handle text for topup amount ----------
@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message):
    user_id, chat_id, text = message.from_user.id, message.chat.id, message.text.strip()

    if user_id not in pending_actions:
        return

    action = pending_actions[user_id]["action"]

    if action == "topup_amount":
        try:
            amount = float(text)
            if amount <= 0:
                raise ValueError("Invalid amount")

            pending_actions.pop(user_id, None)

            payload = {
                "amount": amount,
                "currency": "TONCOIN",   # xRocket currently works with TON
                "description": f"Top-up for {user_id}"
            }
            headers = {"Rocket-Pay-Key": XROCKET_API_KEY}

            resp = requests.post(XROCKET_API_URL, json=payload, headers=headers, timeout=10)
            data = resp.json()

            if data.get("success") and "data" in data:
                pay_url = data["data"].get("payLink") or data["data"].get("link")
                bot.send_message(
                    chat_id,
                    f"✅ Invoice created for **{amount:.2f} TON**\nClick below to pay:",
                    parse_mode="Markdown",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton("💰 Pay Now", url=pay_url),
                        types.InlineKeyboardButton("🔙 Back", callback_data="personal_area")
                    )
                )
            else:
                bot.send_message(chat_id, f"⚠️ Payment error: {data}", reply_markup=personal_area_keyboard())

        except Exception as e:
            pending_actions.pop(user_id, None)
            bot.send_message(chat_id, f"❌ Invalid input. Error: {e}", reply_markup=personal_area_keyboard())
            
# ---------- admin ----------
@bot.message_handler(commands=["stats"])
def stats(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    db = load_db()
    bot.reply_to(message, f"📊 Total users: {len(db)}")

# ---------- run ----------
if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
    