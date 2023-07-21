from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_task_title = State()
    GET_task_description = State()

    CHANGE_task_status = State()