from pprint import pprint

import asyncio
from bson import ObjectId
from motor import motor_asyncio
import motor
from pymongo.errors import DuplicateKeyError

from db_access import search_title_db

conn_str = "mongodb+srv://mteen:QPwklsARMojrZmya@cluster0.fxaegkg.mongodb.net/?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['Books']
collection = db['books']


# return book_dict


async def main():
    # books = await search_title_db('5 am')
    # for book in books:
    #     pprint(book['title'])
    #     pprint(book['_id'])
    #     book_id = book["_id"]
    with open('5am.txt', 'r') as f:
        text = f.read()
    book_id = ObjectId('640091878bf6ee6cf31ea8ab')
    summary = {"_id": book_id, "summary": text}
    result = await db.summary.insert_one(summary)
    print('inserted %d docs' % (len(result.inserted_id),))


if __name__ == "__main__":
    asyncio.run(main())
