import pprint

import motor.motor_asyncio
import motor
import bson


async def search_author_db(name,db):
    cursor = db.books.find({'authors': {
        '$regex': f'(?i){name}(?-i)'
    }}).sort('authors')
    res = []
    for document in await cursor.to_list(length=10):
        pprint.pprint(document)
        res.append(document)

    return res  # books


async def search_title_db(title, db):
    cursor = db.books.find({'title': {
        '$regex': f'(?i){title}(?-i)'
    }}).sort('title')
    # TODO: sort results based on popularity and/or downloads
    res = []
    for document in await cursor.to_list(length=10):
        res.append(document)

    return res  # books


async def get_summary(book_id, db):
    book_id = bson.ObjectId(book_id)
    res = await db.summary.find_one({'_id': book_id})
    return res


async def get_latest_books(db):
    print('searching')
    cursor = db.books.find().sort('_id', -1).limit(10)
    res = []
    for document in await cursor.to_list(length=10):
        res.append(document)
        pprint.pprint(document)
    return res


async def get_server_info(db):
    try:
        print(await db.server_info())
    except Exception:
        print("Unable to connect to the server.")


async def do_insert(db):
    result = await db.some_collection.insert_many()(

        [{'i': i} for i in range(50)])

    print('inserted %d docs' % (len(result.inserted_ids),))


# loop = asyncio.get_event_loop(
if __name__ == '__main__':
    conn_str = "mongodb://localhost:27017"
    # set a 5-second connection timeout
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
    loop = client.get_io_loop()
    books = loop.run_until_complete(search_author_db('', client))
