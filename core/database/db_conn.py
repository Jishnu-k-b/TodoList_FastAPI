from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todos"]
user_collection = db["users"]


def get_todo_collection():
    return collection


def get_user_collection():
    return user_collection
