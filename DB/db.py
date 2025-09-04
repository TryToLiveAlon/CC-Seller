
from pymongo import MongoClient
import config

class DatabaseManager:
    def __init__(self):
        self.clients = {name: MongoClient(uri) for name, uri in config.MONGO_URIS.items()}
        self.dbs = {
            "main": self.clients["main"].get_database(),
            "backup": self.clients["backup"].get_database(),
            "analytics": self.clients["analytics"].get_database(),
        }

    def get_collection(self, db_name="main", collection="users"):
        return self.dbs[db_name][collection]


db_manager = DatabaseManager()
