# This is the configuration file for your bot.

# --- Bot and Admin Settings ---
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [123456789, 987654321]
BOT_USERNAME = "YourGameCardsBot"

# --- Channel and Group Settings ---
FORCE_JOIN_CHANNELS = [
    {
        "username": "YourMainChannel",
        "enabled": True,
    },
    {
        "username": "YourAnnouncementChannel",
        "enabled": False,
    },
]

# --- KYC (Know Your Customer) Settings ---
KYC_ENABLED = True

# --- Other Bot Logic Settings ---
WELCOME_MESSAGE = "Welcome to the virtual game card store!"
CURRENCY = "USD"
MIN_TRANSACTION_AMOUNT = 5.00
