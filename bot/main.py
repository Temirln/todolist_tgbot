from aiogram import Bot,Dispatcher,types
from handlers import start_handler,invalid_answer,on_startup,add_command,get_task_desc,get_task_name,done_task,get_all_tasks,get_task_id
from dotenv import load_dotenv
import os
import asyncio
import logging

from db import BaseModel,User,create_async_engine,proceed_schemas,get_session_maker
from aiogram.filters import Command
from aiogram import F

from utils.stateforms import StepsForm



async def main() -> None:
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()
    logging.basicConfig(level=logging.DEBUG)

    dp.startup.register(on_startup)
    # dp.shutdown.register()

    dp.message.register(start_handler,Command(commands=['start','run']))

    # ADD TASK
    dp.callback_query.register(add_command,F.data == "add_task")
    dp.message.register(get_task_name,StepsForm.GET_task_title)
    dp.message.register(get_task_desc,StepsForm.GET_task_description)

    # LIST TASKS
    dp.callback_query.register(get_all_tasks,F.data == "list_all_task")
    
    # Done Task
    dp.callback_query.register(done_task,F.data == "done_task")  
    dp.message.register(get_task_id,StepsForm.CHANGE_task_status)

    dp.message.register(invalid_answer)



    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())