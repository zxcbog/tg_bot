from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram import html, types, Router
from FSMstates import CommonStates
from .keyboards.keyboards import work_markup, menu_markup
from utils import *
from config import info_channels

router = Router()
menu_photo = FSInputFile("./imgs/menu_img.png")


@router.message(F.text == "Меню", lambda msg: msg.chat.id not in info_channels)
async def get_menu(message: Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if await state.get_state() is not None:
        await message_with_timer(
            bot=message.bot,
            text="Чтобы выполнить это действие, вернитесь в меню(кнопка \"Назад в меню\" или /start)!",
            chat_id=message.chat.id,
            time=3
        )
        return
    state_data = await state.get_data()
    menu_msg_id = state_data.get("main_menu_msg_id")
    if menu_msg_id:
        await message.bot.delete_message(state.key.chat_id, message_id=menu_msg_id)
    msg = await message.answer_photo(menu_photo, reply_markup=menu_markup)
    await state.update_data(main_menu_msg_id=msg.message_id)


@router.message(CommandStart(), lambda msg: msg.chat.id not in info_channels)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    prev_bot_message = state_data.get("prev_bot_message")
    menu_msg_id = state_data.get("main_menu_msg_id")
    service_messages = state_data.get("service_messages")
    if prev_bot_message:
        await message.bot.delete_message(chat_id=state.key.chat_id, message_id=prev_bot_message)
    if menu_msg_id:
        await message.bot.delete_message(chat_id=state.key.chat_id, message_id=menu_msg_id)
    await state.clear()
    res = await user_registration_check(message.from_user.id)
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Меня зовут Артем!\n"
                             "📦 Оказываем следующие услуги:\n"
                             "👉 Забор груза из любой точки России.  Доставка товара на склады WB, основной маршрут Казань-Москва-Казань.\n"
                             "👉 Фулфилмент в Казани.\n\n"
                             "🕒 Мы экономим ваше время.\n"
                             "📩 Звоните, пишите - @ArtemWBKazan\n"
                             "☎️ 89179202931  (WhatsApp)\n"
                             "💡 Работаем 7 дней в неделю - мы гарантируем своевременное и качественное выполнение всех задач.\n"
                             "Ссылка-приглашение в нашу группу: https://t.me/+ntpE-LxkhZ8wZGQ6\n\n"
                             "После завершения заявки с Вами свяжется менеджер!\n")
    if not res:
        button = KeyboardButton(text="Зарегистрироваться", request_contact=True)
        markup = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)
        await state.set_state(CommonStates.awaiting_contact)
        await message.answer(f"Для начала работы нажмите на кнопку \"Зарегистрироваться\". 😃",
                             reply_markup=markup)
    else:
        await message.answer(f"Вы уже зарегистрированы! Чтобы пользоваться ботом, нажмите на кнопку \"Меню\" внизу 😊",
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


@router.message(F.text, lambda msg: msg.chat.id not in info_channels)
async def unknown_message(message: Message) -> None:
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message_with_timer(
        bot=message.bot,
        text=f"Неизвестная команда. Для продолжения работы нажмите кнопку \"Меню\" или напишите \"Меню\".",
        chat_id=message.chat.id,
        time=3,
    )