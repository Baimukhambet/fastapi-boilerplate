from bson.objectid import ObjectId
from pymongo.database import Database



class APIRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, user_id, post: dict):
        payload = {
            "type": post["type"],
            "price": post["price"],
            "address": post["address"],
            "area": post["area"],
            "rooms_count": post["rooms_count"],
            "description": post["description"],
            "media": []
        }
        payload["user_id"] = ObjectId(user_id)

        result = self.database["posts"].insert_one(payload)
        return result.inserted_id

    def get_post_by_id(self, post_id: str):
        post_object_by_id = ObjectId(post_id)
        post = self.database["posts"].find_one(
            {
                "_id": post_object_by_id,
            }
        )
        # if user_id == post["user_id"]:
        return post
    
    def update_post_by_id(self, post_id: str, new_data: dict, user_id):
        post_object_id = ObjectId(post_id)
        post = self.database["posts"].find_one({"_id": post_object_id})

        if user_id == ObjectId(post["user_id"]):
            self.database["posts"].update_one(
                {"_id": post_object_id},
                {"$set": new_data}
            )

    def delete_post_by_id(self, post_id: str):
        self.database["posts"].delete_one(
            {
                "_id": ObjectId(post_id)
            }
        )
    
    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user


