from pymongo import MongoClient, errors
import config
import os, json, hashlib
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.use_json = False
        self.json_file = "users.json"

        try:
            self.clients = {name: MongoClient(uri, serverSelectionTimeoutMS=3000)
                            for name, uri in config.MONGO_URIS.items()}
            # Force connection test
            self.clients["main"].admin.command("ping")
            self.dbs = {
                "main": self.clients["main"].get_database(),
                "backup": self.clients["backup"].get_database(),
                "analytics": self.clients["analytics"].get_database(),
            }
            print("✅ Connected to MongoDB")
        except errors.ServerSelectionTimeoutError:
            print("⚠️ MongoDB not available, using JSON file as storage.")
            self.use_json = True
            if not os.path.exists(self.json_file):
                with open(self.json_file, "w") as f:
                    json.dump([], f)

    def get_collection(self, db_name="main", collection="users"):
        if self.use_json:
            return None  # JSON mode doesn't use collections
        return self.dbs[db_name][collection]

    # --- JSON Fallback Methods ---
    def load_json(self):
        with open(self.json_file, "r") as f:
            return json.load(f)

    def save_json(self, data):
        with open(self.json_file, "w") as f:
            json.dump(data, f, indent=2)


db_manager = DatabaseManager()
