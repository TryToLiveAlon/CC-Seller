import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "")
CHANNEL_1 = os.getenv("CHANNEL_1", "@your_channel_1")
CHANNEL_2 = os.getenv("CHANNEL_2", "@your_channel_2")
WELCOME_MEDIA_URL = "https://i.ibb.co/ynsqhSXz/IMG-20250209-162258-906.jpg"
# Multiple admin IDs separated by commas in .env
ADMIN_IDS = set(int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit())
XROCKET_API_KEY = os.getenv("XROCKET_API_KEY", "edad082d27343f45ca6a72e9e")
XROCKET_API_URL = "https://pay.xrocket.tg/tg-invoices"
# Rewards
REFS_FOR_COOKIE = int(os.getenv("REFS_FOR_COOKIE", 100))
COOKIE_REWARD_AMOUNT = float(os.getenv("COOKIE_REWARD_AMOUNT", 1.0))

# File storage
DATA_FILE = "users.json"
