<a href="https://codeclimate.com/github/iwatkot/sqlplaybot/maintainability"><img src="https://api.codeclimate.com/v1/badges/d9b5d95be375bb8b00b0/maintainability" /></a>

## How and why

This Telegram bot is build on `aiogram` and `psycopg2` libraries and is needed for fast and simple SQL requests practicing.<br>
You don't need to bother you with setting up the server and database whenever you want to practice or check some SQL requests. The bot will automatically create an empty database for you and if you want you can recreate it just with one command. Yes, it's that simple: start the bot and you already can work with your database.

## Under the hood

The bot uses PostgreSQL and creating a unique user and a database whenever the telegram user starts the bot with `/start` command. After database is ready, the bot will expect that every message from the user is an SQL request. It will open a connection, execute query, fetch results and close the connection. If there will be any results to fetch, or if an error will raise, the bot will return it to the telegram user.<br>
The bot has two locales: **EN** and **RU**. By default it will use English locale, unless the message from telegram user will be sent from a **ru** client.<br>
Locales and all log templates are stored in the **templates** folder in JSON files.

## Available commands

`/start` - default Telegram command to start a bot. It will create a user and a database and welcomes the telegram user with a small guide of how to use the bot.<br>
`/help` - shows important information about how the bot works and familiarizes the user with bot commands.<br>
`/reload` - deletes the current user database and then creates a new one.<br>
`/random` - creates a random table with content in user's database, then returns the table's name to the telgram user.<br>
`/bugreport` - obviously for bugreport, but right now it needs a sane implementation

## Modules
`connection.py` - uses **psycopg2** and **decouple**. Handles the connection to the database (creates connection and closing it).<br>
`logger.py` - handles logging from all modules.<br>
`manage_dbs.py` - uses **psycopg2**. Handles creation and deleting databases from the server. Also handles the main bot function for executing queries on the server.<br>
`manage_users.py` - uses **psycopg2**. Handles creating, deleting and changing the permissions of users.<br>
`generator.py` - uses **psycopg2** and **random_word** for random table creation. **Badly needs a refactoring** or a complete rebuild due to it's awful state right now.<br>
`templates_handler.py` - needed for unpacking templates and formatting database responses.<br>
`main.py` - uses **aiogram**, **asyncio** and **decouple**. The bot's main script, responsible for the behavior of the bot. Needs refactoring and standartization of functions due to the almost similar code.<br>

## To-Do

1. Tests (in work).<br>
2. Sane bugreport feature. :D <br>
3. generator.py refactoring
4. Scheduled auto-clear.<br>
5. Admin commands.<br>
6. Limitations for users.<br>
7. Blacklist for users.<br>
???<br>
PROFIT!

## Changelog
**2023/01/16** - Added README.md<br>
**2023/01/16** - Added MD2 formatting for responses from DB<br>
**2023/01/15** - Added `ru` locale