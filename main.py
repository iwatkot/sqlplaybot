import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config

from logger import write_to_botlog, write_bug_report
from templates_handler import get_templates, fetch_formatter
from manage_users import manage_user, user_permissions
from manage_dbs import manage_db, execute_query
from generator import random_table

TOKEN = config('TOKEN')
USER_MESSAGES = get_templates('user')

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class Form(StatesGroup):
    bugreport = State()


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    # Handles the '/start' command.
    tg_id, uid, lang, user_name = unpack_message(message)
    await message.reply(USER_MESSAGES[lang][message.text].format(user_name))
    await asyncio.sleep(1)
    await bot.send_message(
        tg_id, USER_MESSAGES[lang]["TOUR"], parse_mode='MarkdownV2')
    manage_user(uid, 'CREATE')
    user_permissions(uid, 'ALTER')
    manage_db(uid, 'CREATE')
    await bot.send_message(
        tg_id, USER_MESSAGES[lang]["LETSGO"], parse_mode='MarkdownV2')


@dp.message_handler(commands=["reload"])
async def reload_handler(message: types.Message):
    # Handles the '/reload' command.
    tg_id, uid, lang, user_name = unpack_message(message)
    manage_db(uid, 'DROP')
    manage_db(uid, 'CREATE')
    await bot.send_message(
        tg_id, USER_MESSAGES[lang]["RELOADED"], parse_mode='MarkdownV2')


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    # Handles the '/help' command.
    tg_id, uid, lang, user_name = unpack_message(message)
    await bot.send_message(
        tg_id, USER_MESSAGES[lang]["HELP"], parse_mode='MarkdownV2')


@dp.message_handler(commands=["random"])
async def random_handler(message: types.Message):
    # Handles the '/random' command.
    tg_id, uid, lang, user_name = unpack_message(message)
    response_from_db = random_table(uid)
    if response_from_db == 'CONNECTION_FAILED':
        await bot.send_message(tg_id, USER_MESSAGES[lang][response_from_db])
    elif response_from_db:
        await bot.send_message(
            tg_id, USER_MESSAGES[lang]["RANDOM"].format(response_from_db),
            parse_mode='MarkdownV2')


@dp.message_handler(commands=["bugreport"])
async def bugreport_handler(message: types.Message):
    # Handles the '/bugreport' command.
    tg_id, uid, lang, user_name = unpack_message(message)
    await Form.bugreport.set()
    await message.reply(
        USER_MESSAGES[lang][message.text].format(user_name),
        parse_mode='MarkdownV2')


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    tg_id, uid, lang, user_name = unpack_message(message)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(USER_MESSAGES[lang][message.text])


@dp.message_handler(state=Form.bugreport)
async def process_name(message: types.Message, state: FSMContext):
    tg_id, uid, lang, user_name = unpack_message(message)
    await state.finish()
    write_bug_report(message.text, uid, user_name)
    await message.reply(USER_MESSAGES[lang]["BUG_REPORTED"].format(user_name))


@dp.message_handler()
async def message_handler(message: types.Message):
    # Handles messages which not contain any command.
    tg_id, uid, lang, user_name = unpack_message(message)
    query = message.text
    response_from_db = execute_query(uid, query)
    if response_from_db == 'CONNECTION_FAILED':
        await bot.send_message(tg_id, USER_MESSAGES[lang][response_from_db])
    elif response_from_db:
        await bot.send_message(
            tg_id, fetch_formatter(response_from_db), parse_mode='MarkdownV2')


def unpack_message(message):
    # Extractng data from message.
    tg_id = message.from_user.id
    uid = 'id' + str(tg_id)
    lang = message.from_user.language_code
    lang = lang if lang == 'ru' else 'en'
    user_name = message.from_user.first_name
    write_to_botlog(uid, lang, message.text)
    return tg_id, uid, lang, user_name


if __name__ == "__main__":
    executor.start_polling(dp)
