# --- Bot and Admin Settings ---
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
API_ID = 123456     # from https://my.telegram.org
API_HASH = "YOUR_API_HASH"
ADMIN_IDS = [123456789, 987654321]
BOT_USERNAME = "YourGameCardsBot"
SUPPORT_ID = "@Gamebit"

# --- Channel and Group Settings ---
FORCE_JOIN_CHANNELS = [
    {"username": "YourMainChannel", "enabled": True},
    {"username": "YourAnnouncementChannel", "enabled": False},
]

# --- Other Bot Logic Settings ---
WELCOME_MESSAGE = "Welcome to the virtual game card store!"
CURRENCY = "USD"
START_IMG = ""
MENU_IMG = ""

# --- MongoDB Config ---
MONGO_URIS = {
    "main": "mongodb+srv://username:password@cluster0.mongodb.net/mainDB",
    "backup": "mongodb+srv://username:password@cluster0.mongodb.net/backupDB",
    "analytics": "mongodb+srv://username:password@cluster0.mongodb.net/analyticsDB",
}
