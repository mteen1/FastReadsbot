import pprint

import motor.motor_asyncio
import asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)


db = client.FastReadsbot

async def do_insert(document):

    result = await db.books.insert_one(document)
    print('result %s' % repr(result.inserted_id))


# async def do_insert():
#
#     result = await db.test_collection.insert_many(
#
#         [{'i': i} for i in range(2000)])
#
#     print('inserted %d docs' % (len(result.inserted_ids),))
#

async def do_find():
    document = await db.test_collection.find_one({'author': {'$regex': 'Oak'}})

    pprint.pprint(document)


loop = client.get_io_loop()
# loop.run_until_complete(do_insert())
loop.run_until_complete(do_find())
