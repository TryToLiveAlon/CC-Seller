from .db import db_manager
import hashlib
from datetime import datetime

class UserDB:
    def __init__(self):
        if not db_manager.use_json:
            self.collection = db_manager.get_collection("main", "users")

    def _generate_hash(self, user_id):
        return hashlib.sha256(str(user_id).encode()).hexdigest()[:10]

    def add_user(self, user_id, username):
        if db_manager.use_json:
            users = db_manager.load_json()
            if not any(u["user_id"] == user_id for u in users):
                new_user = {
                    "user_id": user_id,
                    "username": username,
                    "balance": 0,
                    "hash": self._generate_hash(user_id),
                    "created_at": str(datetime.utcnow())
                }
                users.append(new_user)
                db_manager.save_json(users)
        else:
            if not self.collection.find_one({"user_id": user_id}):
                self.collection.insert_one({
                    "user_id": user_id,
                    "username": username,
                    "balance": 0,
                    "hash": self._generate_hash(user_id),
                    "created_at": str(datetime.utcnow())
                })

    def get_user(self, user_id):
        if db_manager.use_json:
            users = db_manager.load_json()
            return next((u for u in users if u["user_id"] == user_id), None)
        return self.collection.find_one({"user_id": user_id})

    def update_balance(self, user_id, amount):
        if db_manager.use_json:
            users = db_manager.load_json()
            for u in users:
                if u["user_id"] == user_id:
                    u["balance"] += amount
            db_manager.save_json(users)
        else:
            self.collection.update_one(
                {"user_id": user_id},
                {"$inc": {"balance": amount}}
            )

user_db = UserDB()
