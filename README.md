
# FastReads

FastReads is a Python Telegram bot that allows users to search for books and provides a summary of the book using MongoDB and the Python Telegram Bot (PTB) library. The bot supports both Persian and English languages.

FastReads searches for books based on user input and retrieves a summary of the book.

You can add books to your database using Google book api and summarize with other tools. Then use the scripts in `/scripts` directory.

The book names and their summaries are stored in the `Books` database in the `books` and `summary` collections respectively. In the future, user collections will be added to allow users to store their favorite books.

This project was originally dockerized, but that version is no longer available.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`bot_token`

`db_connection`

`admin_chat`


## Setup

### create a database

You can have either a local MongoDB database or
a MongoDB Atlas database set up to store and retrieve data. 
* To set up a local database, install MongoDB and create a new database by running mongod and mongo commands.

* For MongoDB Atlas, sign up and follow the setup instructions on their website. 

finally add you database connection string to your .env file.
It should be similar to this:

`mongodb+srv://username:password@clustername.fxaegkg.mongodb.net/?retryWrites=true&w=majority`

note: make sure to name your database `Books` and your collections `books` and `summary`
### Run Locally
Clone the project

```bash
  git clone https://github.com/mtinmh/FastReadsbot
```

Go to the project directory

```bash
  cd FastReadsbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
python main.py
```


## Screenshots

![App Screenshot](/screenshots/1.png)
![App Screenshot](/screenshots/2.png)
