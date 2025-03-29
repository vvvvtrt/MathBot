"""
Клавиатуры преподавателя
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def teacher_kb():
    buttons = [
        [InlineKeyboardButton(text="Посмотреть/добавить узоры", callback_data="look_or_add_patterns")],
        [InlineKeyboardButton(text="Дать дз ученикам", callback_data="home_tasks")],
        [InlineKeyboardButton(text="Назад", callback_data="start")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def teacher_login_kb():
    buttons = [
        [InlineKeyboardButton(text="Это мое устройство", callback_data="check_device")],
        [InlineKeyboardButton(text="Войти по паролю", callback_data="password")],
        [InlineKeyboardButton(text="Назад", callback_data="start")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def look_or_add_patterns_kb():
    buttons = [
        [InlineKeyboardButton(text="Добавить узор", callback_data="add_pattern")],
        [InlineKeyboardButton(text="Назад", callback_data="teacher")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def return_to_login_kb():
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="teacher_login")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def return_to_menu_kb():
    buttons = [
        [InlineKeyboardButton(text="Назад в меню", callback_data="teacher")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def home_task_kb():
    buttons = [
        [InlineKeyboardButton(text="Все верно, выбрать ученика", callback_data="choose_student")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="teacher")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def send_home_task_kb(nicname):
    buttons = [
        [InlineKeyboardButton(text=f"Отправить {nicname}", callback_data="sent_home_task")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="teacher")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

