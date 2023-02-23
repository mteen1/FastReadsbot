import aiohttp
import asyncio

async def search_books(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def main():
    query = 'python programming'
    book_results = await search_books(query)
    for book in book_results['items']:
        print(book['volumeInfo']['title'])

asyncio.run(main())

