from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram import html, types, Router
from FSMstates import CommonStates
from utils import *

work_markup = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Меню")
]], resize_keyboard=True, one_time_keyboard=True)


router = Router()


@router.message(F.text == "Меню")
async def get_menu(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сделать заказ", callback_data="make_offer")],
        [InlineKeyboardButton(text="Мои заказы", callback_data="get_offers")],
        [InlineKeyboardButton(text="Мои данные", callback_data="get_user_info")]
    ])
    await message.answer(f"MENU", reply_markup=markup)


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    result = await db.tasks_handler(f"SELECT * FROM users WHERE telegram_user_id={message.from_user.id}")
    if not result:
        button = KeyboardButton(text="Зарегистрироваться", request_contact=True)
        markup = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)
        await state.set_state(CommonStates.awaiting_contact)
        await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\n"
                             f"Мы ... - транспортная компания, занимающаяся доставкой Ваших товаров Wildberries. 🚚\n"
                             f"Для начала работы нажмите на кнопку \"Зарегистрироваться\". 😃",
                             reply_markup=markup)
    else:
        await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\n"
                             f"Вы уже зарегистрированы! Чтобы пользоваться ботом, нажмите на кнопку \"Меню\" внизу 😊",
                             reply_markup=work_markup)


@router.message(F.contact, CommonStates.awaiting_contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    phone_number = contact.phone_number
    user_id = contact.user_id
    first_name, last_name = contact.first_name, contact.last_name
    query = f"INSERT INTO users(phone_number, first_name, telegram_user_id, last_name) VALUES (" \
            f"'{phone_number}', " \
            f"'{first_name}', " \
            f"{user_id}, " \
            f"'{'Не указано' if not last_name else last_name}'" \
            f")"
    result = await db.tasks_handler(query)
    await state.clear()
    await message.reply(f"Спасибо, ваш номер {phone_number} сохранен!", reply_markup=work_markup)


@router.message(CommonStates.awaiting_contact)
async def process_contact(message: Message) -> None:
    button = KeyboardButton(text="Зарегистрироваться", request_contact=True)
    markup = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f"Для продолжения работы, вам нужно зарегистрироваться!",
                         reply_markup=markup)