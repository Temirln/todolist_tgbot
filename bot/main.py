from aiogram import Bot, Dispatcher
from handlers import (
    start_handler,
    invalid_answer,
    on_startup,
    on_shutdown,
    add_command,
    get_task_desc,
    get_task_name,
    done_task,
    get_all_tasks,
    change_task_by_id,
    delete_task,
    delete_task_by_id,
    show_keyboard,
)
from dotenv import load_dotenv
import os
import asyncio

from aiogram.filters import Command
from aiogram import F

from utils.stateforms import StepsForm


async def main() -> None:
    load_dotenv()
    bot = Bot(os.getenv("TOKEN"))
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.register(start_handler, Command(commands=["start", "run"]))
    dp.message.register(show_keyboard, Command(commands=["keyboard"]))

    # ADD TASK
    dp.callback_query.register(add_command, F.data == "add_task")
    dp.message.register(get_task_name, StepsForm.GET_task_title)
    dp.message.register(get_task_desc, StepsForm.GET_task_description)

    # LIST TASKS
    dp.callback_query.register(get_all_tasks, F.data == "list_all_task")

    # Done Task
    dp.callback_query.register(done_task, F.data == "done_task")
    dp.message.register(change_task_by_id, StepsForm.CHANGE_task_status)

    # Delete Task
    dp.callback_query.register(delete_task, F.data == "delete_task")
    dp.message.register(delete_task_by_id, StepsForm.DELETE_task_by_id)

    # Other Message Handler
    dp.message.register(invalid_answer)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
