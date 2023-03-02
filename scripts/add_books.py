from pprint import pprint
import aiohttp
import asyncio
import motor
import motor.motor_asyncio
from datetime import datetime

from pymongo.errors import DuplicateKeyError


async def search_books(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1'   # &maxResults=1
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data


# connect to MongoDB Atlas
conn_str = "mongodb+srv://mteen:QPwklsARMojrZmya@cluster0.fxaegkg.mongodb.net/?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['Books']
collection = db['books']


def parse_book(book):
    book = book['volumeInfo']
    # parse the JSON response to get book details
    title = book.get('title', None)
    authors = book.get('authors', None)
    publisher = book.get('publisher', None)
    publishedDate = None
    if 'publishedDate' in book:
        try:
            publishedDate = book['publishedDate']
        except ValueError:
            pass
    description = book.get('description', None)
    industryIdentifiers = book.get('industryIdentifiers', None)
    categories = book.get('categories', None)

    # create a dictionary for the book details
    book_dict = {
        'title': title,
        'authors': authors,
        'publisher': publisher,
        'publishedDate': publishedDate,
        'industryIdentifiers': industryIdentifiers,
        'categories': categories
    }
    return book_dict


async def main():
    file = open('books.txt', 'r')
    books = file.readlines()
    for query in books:
        book_results = await search_books(query.strip())
        for book in book_results['items']:
            book_dict = parse_book(book)
            # insert the book into the database
            try:
                result = await collection.insert_one(book_dict)
                print(f'Book inserted with ID: {result.inserted_id}')
            except DuplicateKeyError:
                print('Duplicate book, skipping this one')
                pass
            # print the ID of the inserted book


asyncio.run(main())

