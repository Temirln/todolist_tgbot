from aiogram import Bot,Dispatcher,executor,types
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f"Доро пожаловать {message.from_user.full_name}, в To Do List телеграм бот")

@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я ваc не понял')

if __name__ == "__main__":
    executor.start_polling(dp)
