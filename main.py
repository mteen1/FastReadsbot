import logging

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler
from api_key import TOKEN
from db_funcs import search_title_db, search_author_db
import motor
import motor.motor_asyncio
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


conn_str = "mongodb://172.18.0.2"

# set a 5-second connection timeout
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: add book id handler to send related gateway
    print(update.message.text[7:])
    search_buttons = [
        [
            InlineKeyboardButton("محبوب🔥", switch_inline_query_current_chat='popular'),
            InlineKeyboardButton("جدیدترین ها🆕", switch_inline_query_current_chat='new'),
        ],
        [
            InlineKeyboardButton("جستجو بر اساس عنوان", switch_inline_query_current_chat=''),
            InlineKeyboardButton("جستجو بر اساس نویسنده", switch_inline_query_current_chat='author: '),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(search_buttons)
    await update.message.reply_text(reply_markup=reply_markup,
                                    text=f"سلام {update.effective_chat.first_name}!\nدیگه با خوندن کتاب های طولانی خداحافظی کن! 😊"
                                         f"\nبا  FastReads میتونی به راحتی کتاب های مورد علاقتو پیدا کنی و خلاصه جامع و نکات کلیدی رو مستقیما دریافت کنی.📚 "
                                         f"\nبرای شروع روی یکی از دکمه های زیر کلیک کن")


async def send_gateway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text[7:]
    keyboard = [[
        InlineKeyboardButton('خرید', url='www.google.com')
    ]]
    # book_info = search_info() #TODO:get info from db
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(reply_markup=reply_markup, text=f'query is {query}')


# Different types of inline searches
async def inline_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    books = await search_title_db(query)
    results = []
    format_results(results, books)
    # print(f'these are the results:{results}')
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def inline_author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query[7:].strip()
    print(f'searching for {query}.....')
    books = await search_author_db(query)
    results = []
    format_results(results, books)
    await context.bot.answer_inline_query(update.inline_query.id, results)


# formats the data retrieved form db
def format_results(results, books):
    # format the results and add them to the results list
    for book in books:
        keyboard = [
            [
                InlineKeyboardButton("خرید کتاب", url=f"https://t.me/FastReadsbot?start={book['_id']}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        results.append(
            InlineQueryResultArticle(
                id=book['_id'],
                title=book['title'],
                description=book['author'],
                reply_markup=reply_markup,
                input_message_content=InputTextMessageContent(f"نام کتاب: {book['title']}\n"
                                                              f"نویسنده: {book['author']}\n"

                                                              )
            )
        )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    summary_handler = CommandHandler('start', send_gateway, filters=filters.Regex('^/start\s+.+'))
    start_handler = CommandHandler('start', start, filters=filters.Regex('^/start$'))
    inline_author_handler = InlineQueryHandler(inline_author, pattern=r'author: \w{3,}')
    inline_title_handler = InlineQueryHandler(inline_title)

    # inline_new_handler = InlineQueryHandler(inline_new, pattern=r'new')
    # inline_popular_handler = InlineQueryHandler(inline_popular, pattern=r'popular')
    # unknown_handler = MessageHandler(filters.COMMAND, start)

    # TODO: add new and popular books
    # application.add_handler(inline_popular_handler)
    # application.add_handler(inline_new_handler)
    application.add_handler(start_handler)
    application.add_handler(summary_handler)
    application.add_handler(inline_author_handler)
    application.add_handler(inline_title_handler)
    # application.add_handler(unknown_handler)

    application.run_webhook(
        listen='0.0.0.0',
        port=80,
        key='private.key',
        cert='cert.pem',
        webhook_url='https://fastreads.onrender.com:80'
    )
