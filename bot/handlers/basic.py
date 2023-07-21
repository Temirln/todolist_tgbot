from aiogram import types
from keyboards import get_todolist_inline_keyboard
from db import (
    start_db,
    add_user,
    add_task,
    get_tasks,
    change_task_status,
    delete_task_from_db,
)
from aiogram.fsm.context import FSMContext
from utils.stateforms import StepsForm


async def on_startup():
    await start_db()
    print("Bot started")


async def start_handler(message: types.Message):
    await add_user(message.from_user.username, message.from_user.id)
    await message.answer(
        f"Добро пожаловать {message.from_user.full_name}, в To Do List телеграм бот",
        reply_markup=get_todolist_inline_keyboard(),
    )


async def add_command(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите название таска")
    await state.set_state(StepsForm.GET_task_title)


async def get_task_name(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Теперь введите Описание таска")
    await state.set_state(StepsForm.GET_task_description)


async def get_task_desc(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)

    context_data = await state.get_data()
    await message.answer(f"Saved data in FSM:{context_data}")
    title = context_data.get("title")
    description = context_data.get("desc")
    owner_id = message.from_user.id

    await add_task(title, description, owner_id)
    await state.clear()


async def get_all_tasks(call: types.CallbackQuery):
    await call.message.reply(await get_tasks(call.from_user.id))


async def done_task(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите Индекс таска статус которого хотите изменить")
    await state.set_state(StepsForm.CHANGE_task_status)


async def change_task_by_id(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.reply("Нужно ввести Индекс Таска")
        return

    result = await change_task_status(message.text, message.from_user.id)
    if result:
        await message.reply("Статус Таска успешно изменен")
        await state.clear()
        return
    await message.reply("Неправильный индекс таска")


async def delete_task(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите Индекс таска статус которого хотите удалить")
    await state.set_state(StepsForm.DELETE_task_by_id)


async def delete_task_by_id(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.reply("Нужно ввести индекс Таска")
        return
    result = await delete_task_from_db(message.text, message.from_user.id)
    if result:
        await message.reply("Таск Был удален")
        await state.clear()
        return
    await message.reply("Неправильный Индекс Таска")


async def invalid_answer(message: types.Message):
    # await message.answer(message.from_user.id)
    await message.reply("Я вас не понял")
