"""
Обработчики для учителя
"""
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from pydantic.v1.validators import anystr_strip_whitespace

import config
from bot.keyboards.start import start_kb
from bot.keyboards.teacher import teacher_kb, teacher_login_kb, return_to_login_kb, return_to_menu_kb, \
    look_or_add_patterns_kb, home_task_kb, send_home_task_kb
from config import bot, dp
from aiogram.types import CallbackQuery, Message


class AuthState(StatesGroup):
    wait = State()


class PatternState(StatesGroup):
    wait = State()


class GiveHomeTask(StatesGroup):
    wait = State()
    choosing = State()


@dp.callback_query(F.data == "teacher_login")
async def teacher_login(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Для начала вам нужно войти.\nКак вы бы хотели это сделать?",
        reply_markup=teacher_login_kb()
    )


@dp.callback_query(F.data == "check_device")
async def teacher_login_by_id(callback: CallbackQuery):
    db_admin_id = 1  # todo вставить проверку айдишника из бд
    if db_admin_id == callback.from_user.id:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Добро пожаловать!\nЭто ваша домашняя страница тут вы можете...",
            reply_markup=teacher_kb()
        )
    else:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Зачем врать? =(",
            reply_markup=return_to_login_kb()
        )


@dp.callback_query(F.data == "password")
async def teacher_login_by_password(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Введите пароль",
        reply_markup=return_to_login_kb()
    )
    await state.update_data(call=callback)
    await state.set_state(AuthState.wait)


@dp.message(StateFilter(AuthState.wait))
async def password_typing(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.delete()
    await validate_password(state)


async def validate_password(state: FSMContext):
    data = await state.get_data()
    password = data["password"]
    call = data["call"]

    # todo достать пароли из бд (желательно все, потому что вход по паролю для того и нужен, что у тя нет конкретного айдишника)
    db_password = config.admin_password
    if password == db_password:  # должно быть if password in db_passwords
        await call.message.edit_text(
            text="Добро пожаловать!\nЭто ваша домашняя страница тут вы можете...",
            reply_markup=teacher_kb()
        )
    else:
        await call.message.edit_text(
            text="Пароль неверный =(",
            reply_markup=return_to_login_kb()
        )


@dp.callback_query(F.data == "teacher")
async def teacher(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Это ваша домашняя страница тут вы можете...",
        reply_markup=teacher_kb()
    )


@dp.callback_query(F.data == "look_or_add_patterns")
async def look_or_add_patterns(callback: CallbackQuery, state: FSMContext):
    await state.update_data(call=callback)
    await display_patterns(state)


async def display_patterns(state: FSMContext):
    data = await state.get_data()
    call = data["call"]
    new_pattern = data.get("new_pattern", "")

    if new_pattern == "":
        # todo запрос из бд на все добавленные рисунки
        db_request = ["Хохма", "Хохма", "Хохма", "Хохма"]
        patterns_str = "\n".join([i for i in db_request])
        await call.message.edit_text(
            text="Ваши узоры: \n" + patterns_str,
            reply_markup=look_or_add_patterns_kb()
        )
    else:
        # todo запись нового паттерна в бд мб
        # db_request = [] #с возвратом всех паттернов если хотим сразу и отображать после добавления
        # patterns_str = "\n".join([i for i in db_request])
        await call.message.edit_text(
            text="Новый узор успешно добавлен\n\n",
            reply_markup=return_to_menu_kb()
        )
    await state.clear()


@dp.callback_query(F.data == "add_pattern")
async def add_pattern(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Введите новый паттерн",
        reply_markup=return_to_menu_kb()
    )
    await state.update_data(call=callback)
    await state.set_state(PatternState.wait)


@dp.message(StateFilter(PatternState.wait))
async def pattern_typing(message: Message, state: FSMContext):
    await state.update_data(new_pattern=message.text)
    await message.delete()
    await display_patterns(state)


@dp.callback_query(F.data == "home_tasks")
async def home_tasks(callback: CallbackQuery, state: FSMContext):
    # todo получить все узоры
    patterns = ["Хохма", "Хохма", "Хохма", "Хохма", "Хохма", "Хохма", "Хохма", "Хохма", "Хохма", "Хохма", "Хохма"]
    patterns_str = "\n".join([i for i in patterns])
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Напишите по каким узорам дать дз через пробел\n\n" + patterns_str,
        reply_markup=return_to_menu_kb()
    )
    await state.update_data(call=callback)
    await state.set_state(GiveHomeTask.wait)


@dp.message(StateFilter(GiveHomeTask.wait))
async def patterns_typing(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()

    callback = data["call"]
    patterns = "\n".join([i for i in message.text.split(" ")])

    await callback.message.edit_text(
        text=f"Выбранные узоры:\n\n{patterns}",
        reply_markup=home_task_kb()
    )
    await state.update_data(patterns=message.text)

@dp.callback_query(F.data == "choose_student")
async def choose_student(callback: CallbackQuery, state: FSMContext):
    #todo достать список учеников
    student_lst = ["Denis", "Ne Denis"]
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выберите и напишите никнейм ученика:\n\n" + "\n".join([i for i in student_lst]),
        reply_markup=return_to_menu_kb()
    )
    await state.update_data(call=callback)
    await state.set_state(GiveHomeTask.choosing)

@dp.message(StateFilter(GiveHomeTask.choosing))
async def generate_task_and_send(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()

    callback = data["call"]
    await state.update_data(nickname=message.text)

    await callback.message.edit_text(
        text=f"Выбранный ученик:\n\n {message.text}",
        reply_markup=send_home_task_kb(message.text)
    )

@dp.callback_query(lambda c: c.data.split("_")[0] == "send")
async def send_home_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = callback.data.split("_")[1]
    nickname = data["nickname"]
    patterns = data["patterns"]

    #todo по никнеймку достаем айди
    #TODO генерим пикчи
    #todo записываем в бд ученику его новое дз
    await callback.answer(text="дз отправлено", show_alert=True)
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Добро пожаловать!\nЭто ваша домашняя страница тут вы можете...",
        reply_markup=teacher_kb()
    )
