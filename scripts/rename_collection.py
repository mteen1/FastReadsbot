import asyncio
import motor.motor_asyncio
import pymongo



conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client.FastReadsbot
old = db.test_collection
new = db.books
old.rename("books")
