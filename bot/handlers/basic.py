from aiogram import types
from keyboards import get_inline_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from db import start_db,add_user,add_task,get_tasks,change_task_status
from aiogram.fsm.context import FSMContext
from utils.stateforms import StepsForm

async def on_startup():
    await start_db()
    print("Bot started")

async def start_handler(message: types.Message): 
    # await session.execute(insert(User).values(tg_user_id = message.from_user.id,username=message.from_user.username))
    await add_user(message.from_user.username,message.from_user.id)
    await message.answer_sticker("CAACAgIAAxkBAAIFOGS5CFJMlrtob-3E0oTOT8XmwBIuAAKrNQACtNoRSZKs_yZJI4DjLwQ")
    await message.answer(f"Добро пожаловать {message.from_user.full_name}, в To Do List телеграм бот",reply_markup=get_inline_keyboard())


async def add_command(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите название таска")
    await state.set_state(StepsForm.GET_task_title)


async def get_task_name(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Теперь введите Описание таска")
    await state.set_state(StepsForm.GET_task_description)

async def get_task_desc(message: types.Message, state: FSMContext):
    await state.update_data(desc = message.text)

    context_data = await state.get_data()
    await message.answer(f"Saved data in FSM:{context_data}")
    title = context_data.get("title")
    description = context_data.get("desc")
    owner_id = message.from_user.id

    await add_task(title,description,owner_id)
    await state.clear()
    # await state.finish()


async def get_all_tasks(call: types.CallbackQuery):
    await call.message.reply(await get_tasks(call.from_user.id))

async def done_task(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите Индекс таска статус которого хотите изменить")
    await state.set_state(StepsForm.CHANGE_task_status)

async def get_task_id(message: types.Message, state: FSMContext):
    await change_task_status(message.text)
    await message.reply("Статус Вашего таска был изменен")
    await state.clear()
    # await state.finish()


async def invalid_answer(message: types.Message):
    # await message.answer(message.from_user.id)
    await message.reply('Я вас не понял')

