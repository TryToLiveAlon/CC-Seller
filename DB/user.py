
from .db import db_manager

class UserDB:
    def __init__(self):
        self.collection = db_manager.get_collection("main", "users")

    def add_user(self, user_id, username):
        if not self.collection.find_one({"user_id": user_id}):
            self.collection.insert_one({
                "user_id": user_id,
                "username": username,
                "balance": 0,
                "created_at": "now"
            })

    def get_user(self, user_id):
        return self.collection.find_one({"user_id": user_id})

    def update_balance(self, user_id, amount):
        self.collection.update_one(
            {"user_id": user_id},
            {"$inc": {"balance": amount}}
        )

user_db = UserDB()
