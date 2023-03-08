import json
import logging
import math
from pprint import pprint

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, \
    CallbackQueryHandler
from db_access import (search_title_db,
                       search_author_db,
                       get_latest_books,
                       get_summary)
import motor
import motor.motor_asyncio
import os
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
# connect to MongoDB Atlas
conn_str = os.getenv('db_connection')
# set a 5-second connection timeout
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['Books']
collection = db['books']

# Load language data from JSON files
with open('lang/en.json', encoding='utf-8') as f:
    en = json.load(f)
with open('lang/fa.json', encoding='utf-8') as f:
    fa = json.load(f)

# Set the default language to Farsi
lang = fa


async def switch_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """changes the language with /switch_lang command"""
    global lang
    if lang == fa:
        lang = en
        await update.message.reply_text('Language set to English!')
    else:
        lang = fa
        await update.message.reply_text('زبان به فارسی تغییر یافت!')
    await start(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = context.user_data
    print(lang_code)

    search_buttons = [
        [
            InlineKeyboardButton(lang['s_title'], switch_inline_query_current_chat=''),
        ],
        [
            InlineKeyboardButton(lang['s_author'], switch_inline_query_current_chat='author: '),
        ],
        [
            InlineKeyboardButton(lang['latest'], switch_inline_query_current_chat='latest'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(search_buttons)
    await update.message.reply_text(reply_markup=reply_markup,
                                    text=lang['start'].format(name=update.effective_chat.first_name))


async def send_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """parse the ObjectId from the query and get the summary from db"""
    query = update.message.text[7:]
    print(f'searching for summary:{query}')
    summary = await get_summary(query, db)
    try:
        summary_text = summary['summary']

        chunk_size = 4096
        num_chunks = math.ceil(len(summary_text) / chunk_size)

        for i in range(num_chunks):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size
            chunk = summary_text[start_index:end_index]
            await update.message.reply_text(chunk)
    except TypeError:
        await update.message.reply_text('Oops! summary not found! :(')

        # send the book id to admin, so it can be added later
        await context.bot.send_message(chat_id=os.getenv('admin_chat'),
                                       text=f"'{query}' summary requested\n----------------------")


# Different types of inline searches
async def inline_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    books = await search_title_db(query, db)
    results = []
    format_results(results, books)
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def inline_author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query[7:]
    print(f'searching for {query}.....')
    books = await search_author_db(query, db)
    results = []
    format_results(results, books)
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def inline_latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    books = await get_latest_books(db)
    print('getting recent books')
    results = []
    format_results(results, books)

    await context.bot.answer_inline_query(update.inline_query.id, results)


# formats the data retrieved form db
def format_results(results, books):
    """format the results to InlineResultArticle and append them to results"""
    for book in books:
        pprint(book)
        keyboard = [
            [
                InlineKeyboardButton(lang['get_summary'], url=f'https://t.me/FastReadsbot?start={book["_id"]}'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        results.append(
            InlineQueryResultArticle(
                id=book['_id'],
                title=book['title'],
                description=', '.join(book['authors']),
                reply_markup=reply_markup,
                input_message_content=InputTextMessageContent(
                    lang["book_info"].format(title=book['title'], author=(', '.join(book['authors'])),
                                             genre=book.get('categories', ''))
                )
            ))


async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=lang['help'])


async def summary_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """sends the summary requests to bot admin"""
    book_name = update.message.text[5:]
    message = await context.bot.send_message(chat_id=os.getenv('admin_chat'),
                                             text=f"'{book_name}' book requested\n----------------------")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('bot_token')).build()

    summary_handler = CommandHandler('start', send_summary, filters=filters.Regex('^/start\s.+'))
    start_handler = CommandHandler('start', start, filters=filters.Regex('^/start$'))
    req_handler = CommandHandler('add', summary_request)
    inline_author_handler = InlineQueryHandler(inline_author, pattern=r'author: \w{3,}')
    inline_latest_handler = InlineQueryHandler(inline_latest, pattern=r'latest')
    inline_title_handler = InlineQueryHandler(inline_title)

    application.add_handler(start_handler)
    application.add_handler(summary_handler)
    application.add_handler(inline_author_handler)
    application.add_handler(inline_title_handler)
    application.add_handler(req_handler)
    application.add_handler(inline_latest_handler)
    application.add_handler(CommandHandler('lang', switch_lang))
    application.add_handler(CommandHandler('help', send_help))

    application.run_polling()
