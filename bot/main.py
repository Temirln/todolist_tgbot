from aiogram import Bot,Dispatcher,executor,types
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add("Корзина").add("Contacts")

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # await message.answer_sticker("CAACAgIAAxkBAAIFOGS5CFJMlrtob-3E0oTOT8XmwBIuAAKrNQACtNoRSZKs_yZJI4DjLwQ")
    await message.answer(f"Доро пожаловать {message.from_user.full_name}, в To Do List телеграм бот",reply_markup=main)

@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    await message.answer(f"Добавить новый таск <задача>")

@dp.message_handler(commands=['done'])
async def add_task(message: types.Message):
    await message.answer(f"Выполнен один таск <индекс>")

@dp.message_handler(commands=['list'])
async def list_of_task(message: types.Message):
    await message.answer(f"Список тасков")


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я ваc не понял')


if __name__ == "__main__":
    executor.start_polling(dp)
