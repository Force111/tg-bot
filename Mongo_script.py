from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()


uri =os.getenv("MONGO_URI")


def Mongo_connect():
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client["learning_linux"]

    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

    return client, db


class Morning:
    def connect(self, db):
        self.collection = db["learning_linux"]

    def morning_script(self):
        print("Morning script in progress!")
        day_info = self.collection.find_one({"status": "in_progress"})
        return day_info

    def progress_check(self, day_info):
        if day_info is None:
            print("No in_progress was found")
            day_info = self.collection.find_one(
                {"status": "todo"},
                sort=[("day", ASCENDING)]
            )

        return day_info

    def status_change(self, day_info):
        if day_info is None:
            return None

        if day_info["status"] != "in_progress":
            day_id = day_info["_id"]

            result = self.collection.update_one(
                {
                    "_id": day_id,
                    "status": "todo",
                },
                {
                    "$set": {"status": "in_progress"},
                },
            )

            if result.modified_count == 1:
                print("Status updated successfully")
                day_info["status"] = "in_progress"
            else:
                print("Status NOT updated (maybe already changed)")
                return None

        return day_info