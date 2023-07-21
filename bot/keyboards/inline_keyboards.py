from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# catalog = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text="Add Task",callback_data="add_task"),
#         InlineKeyboardButton(text="Delete Task",callback_data="delete_task")
#     ],
#     [
#         InlineKeyboardButton(text="Done Task",callback_data="done_task"),
#         InlineKeyboardButton(text="List All Tasks",callback_data="list_all_task")
#     ]
# ])

def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Add Task",callback_data="add_task")
    keyboard_builder.button(text="Delete Task",callback_data="delete_task")
    keyboard_builder.button(text="Done Task",callback_data="done_task")
    keyboard_builder.button(text="List All Tasks",callback_data="list_all_task")

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()