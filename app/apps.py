from fastapi import FastAPI
from pymongo import MongoClient


app = FastAPI()

# MongoDb connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todo"]
