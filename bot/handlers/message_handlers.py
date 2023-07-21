from aiogram import types
from keyboards import get_todolist_inline_keyboard
from db import (
    add_user,
    add_task,
    change_task_status,
    delete_task_from_db,
)
from aiogram.fsm.context import FSMContext
from utils import StepsForm, numeric_message


async def start_handler(message: types.Message):
    await add_user(message.from_user.username, message.from_user.id)

    await message.answer(
        f"Добро пожаловать {message.from_user.full_name}, в To Do List телеграмм бот",
        reply_markup=get_todolist_inline_keyboard(),
    )


async def get_task_name(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Теперь введите Описание таска")
    await state.set_state(StepsForm.GET_task_description)


async def get_task_desc(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)

    context_data = await state.get_data()
    await message.answer(
        "Ваш таск был сохранен\nМожете посмотреть его в списке всех задач"
    )
    title = context_data.get("title")
    description = context_data.get("desc")
    owner_id = message.from_user.id

    await add_task(title, description, owner_id)
    await state.clear()


@numeric_message
async def change_task_by_id(message: types.Message, state: FSMContext):

    result = await change_task_status(message.text, message.from_user.id)
    if result:
        await message.reply("Статус Таска успешно изменен")
        await state.clear()
        return
    await message.reply("Неправильный индекс таска")


@numeric_message
async def delete_task_by_id(message: types.Message, state: FSMContext):

    result = await delete_task_from_db(message.text, message.from_user.id)
    if result:
        await message.reply("Таск Был удален")
        await state.clear()
        return
    await message.reply("Неправильный Индекс Таска")


async def invalid_answer(message: types.Message):
    await message.reply("Я вас не понимаю")
