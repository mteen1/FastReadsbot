import pprint
import motor.motor_asyncio
import motor
# connect to MongoDB Atlas
conn_str = "mongodb+srv://mteen:QPwklsARMojrZmya@cluster0.fxaegkg.mongodb.net/?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['Books']
collection = db['books']


async def search_author_db(name):
    cursor = client.Books.books.find({'authors': {
        '$regex': f'(?i){name}(?-i)'
    }}).sort('authors')
    res = []
    for document in await cursor.to_list(length=10):
        pprint.pprint(document)
        res.append(document)

    return res  # books


async def search_title_db(title):
    cursor = client.Books.books.find({'title': {
        '$regex': f'(?i){title}(?-i)'
    }}).sort('title')  # TODO: sort results based on popularity and/or downloads
    res = []
    for document in await cursor.to_list(length=10):
        res.append(document)

    return res  # books


async def get_server_info(client):
    try:
        print(await client.server_info())
    except Exception:
        print("Unable to connect to the server.")


# async def do_insert():
#     result = await client.test_collection.insert_many()(
#
#         [{'i': i} for i in range(50)])
#
#     print('inserted %d docs' % (len(result.inserted_ids),))
#

# loop = asyncio.get_event_loop(
if __name__ == '__main__':
    loop = client.get_io_loop()
    books = loop.run_until_complete(search_author_db('test'))
    print(books)
