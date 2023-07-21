from aiogram import types
from aiogram.fsm.context import FSMContext


def numeric_message(func):
    async def wrapper(message: types.Message, state: FSMContext):
        if message.text.isnumeric():
            return await func(message, state)
        return message.reply("Нужно ввести Индекс Таска")

    return wrapper
