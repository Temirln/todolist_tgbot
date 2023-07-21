from aiogram import types
from aiogram.fsm.context import FSMContext
from utils import StepsForm
from db import get_tasks
from prettytable import PrettyTable


async def delete_task(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите Индекс таска статус которого хотите удалить")
    await state.set_state(StepsForm.DELETE_task_by_id)


async def get_all_tasks(call: types.CallbackQuery):
    tasks = await get_tasks(call.from_user.id)
    if len(tasks) == 0:
        call.message.reply("Ваш Список дел Пуст")

    # table = [["col", "Title", "Description", "Index", "Status", "Mark"]]
    text = ""
    # tab = PrettyTable(table[0])

    for index, task in enumerate(tasks):
        status = "Не Выполнен"
        status_mark = "❌"
        if task.status:
            status_mark = "✅"
            status = "Выполнен"

        text += f"""{index+1}){task.title}\n   Описание: {task.description}\n   Статус: {status}{status_mark}\n   Индекс: {task.id} \n\n"""
        # table.append(
        #     [index + 1, task.title, task.description, task.id, status, status_mark]
        # )

    # tab.add_rows(table[1:])
    # await call.message.reply(f"<pre>{tab}</pre>", parse_mode="HTML")
    await call.message.answer(text)


async def done_task(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите Индекс таска статус которого хотите изменить")
    await state.set_state(StepsForm.CHANGE_task_status)


async def add_command(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите название таска")
    await state.set_state(StepsForm.GET_task_title)
