"""
Клавиатуры старта
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Ученик", callback_data="student"),
            InlineKeyboardButton(text="Преподаватель", callback_data="teacher_login"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def return_to_start_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Назад", callback_data="start"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard