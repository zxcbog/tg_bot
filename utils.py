from DatabaseIO import DatabaseIO
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from config import *
from aiogram import Bot, html
from aiogram.types import Message, CallbackQuery, Chat
from aiogram.fsm.context import FSMContext
import functools
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import info_channels

loop = asyncio.get_event_loop()
client = AsyncIOMotorClient("mongodb://localhost:27017")

m_db = client["wb_bot"]

db = DatabaseIO(user=user,
                password=passwd,
                database=dbase,
                host=host,
                loop=loop)

registered_users = {}

message_queues = {}

lock = asyncio.Lock()

message_lifetime = 900 # время жизни сообщения, запрашивающего данные


async def clear_state_def(state: FSMContext):
    s = await state.get_state()
    if s is not None:
        await state.clear()


def message_lifetime_check(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)
        if res is None:
            return res
        context_data = args[0]
        state = kwargs['state']
        message_id = None
        if isinstance(context_data, CallbackQuery):
            message_id = context_data.message.message_id
        elif isinstance(context_data, Message):
            message_id = context_data.message_id
        current_FSM_state = await state.get_state()
        await asyncio.sleep(message_lifetime)
        last_FSM_state = await state.get_state()
        if current_FSM_state == last_FSM_state:
            if message_id is not None:
                await context_data.bot.delete_message(chat_id=state.key.chat_id, message_id=res)
                await state.clear()
        return res
    return wrapper


async def update_state(text: str, bot, chat_id: int, user_message_id: int, bot_message_id: int, reply_markup=None):
    if user_message_id is not None:
        await bot.delete_message(chat_id=chat_id, message_id=user_message_id)
    await bot.edit_message_text(text=text, chat_id=chat_id,
                                message_id=bot_message_id, reply_markup=reply_markup)


async def user_registration_check(telegram_user_id: int):
    result = await db.tasks_handler(f"SELECT * FROM users WHERE telegram_user_id={telegram_user_id}")
    return result


async def add_message_to_delete(chat_id: int, message_id: int):
    if not message_queues.get(chat_id):
        message_queues[chat_id] = asyncio.Queue()
    await message_queues[chat_id].put(message_id)


async def delete_old_messages(bot: Bot):
    for chat_id, msg_que in message_queues.items():
        while msg_que.qsize() > 1:
            await bot.delete_message(chat_id=chat_id, message_id=msg_que.get_nowait())


async def create_custom_markup(text_with_callback: tuple):
    return InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text=text_with_callback[0], callback_data=text_with_callback[1])
        ]
    ])

def user_link(user):
    if user.username:
        return html.link(html.bold(user.full_name), f"https://t.me/{user.username}")
    else:
        return html.bold(user.full_name)


async def send_new_order_to_info_channels(bot: Bot, user_id: int):
    order_info_query = "SELECT * FROM orders " \
                 "INNER JOIN users ON users.telegram_user_id = orders.telegram_user_id " \
                 f"WHERE orders.telegram_user_id = {user_id} AND orders.accepted = False"
    order_info = (await db.tasks_handler(order_info_query))[-1]
    chat: Chat = await bot.get_chat(order_info['telegram_user_id'])
    new_order_action_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data=f"new_order_action-yes#{order_info['order_id']},{order_info['telegram_user_id']}"),
            InlineKeyboardButton(text="❌", callback_data=f"new_order_action-no#{order_info['order_id']},{order_info['telegram_user_id']}"),
        ]
    ])
    for info_channel in info_channels:
        await bot.send_message(chat_id=info_channel,
                               text=f"Заказчик: {user_link(chat)}\n"
                                    f"1. Город отправки: {order_info['sending_city']}\n"
                                    f"2. Город доставки: {order_info['delivery_city']}\n"
                                    f"3. Название организации: {order_info['org_name']}\n"
                                    f"4. Адрес загрузки: {order_info['loading_address']}\n"
                                    f"5. Ориентир: {order_info['orientier']}\n"
                                    f"6. Дата и время загрузки: {order_info['loading_datetime']}\n"
                                    f"7. Плановая дата выгрузки: {order_info['delivery_datetime']}\n"
                                    f"8. Упаковка: {order_info['delivery_packaging']}\n"
                                    f"9. Количество: {order_info['delivery_count']}\n"
                                    f"10. Общий вес(кг): {order_info['total_weight']}\n"
                                    f"11. Тип поставки(QR поставка, МоноПалет, Короб, QR приемка): {order_info['delivery_type']}\n"
                                    f"12. Контакт рабочего на загрузке: {order_info['loader_worker_contact']}\n"
                                    f"13. Способ оплаты: {order_info['payment_type']}\n",
                               reply_markup=new_order_action_markup
                               )


async def message_with_timer(bot, text: str, chat_id: int, time: int, message_id_bot:int=None):
    if message_id_bot is None:
        message_id_bot = await bot.send_message(
            text=text,
            chat_id=chat_id, reply_markup=await create_custom_markup((f"{time+1}", "NOT_IMPLEMENTED")))
        message_id_bot = message_id_bot.message_id
    for i in range(time):
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id_bot, reply_markup=await create_custom_markup((f"{time - i}", "NOT_IMPLEMENTED")))
        await asyncio.sleep(1)
    await bot.delete_message(chat_id=chat_id, message_id=message_id_bot)


async def int_validation(message: Message, text:str):
    try:
        result_data = int(message.text)
    except Exception as e:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message_with_timer(
            bot=message.bot,
            text=text + "\n(нужно ввести число)",
            chat_id=message.chat.id,
            time=2
        )
        return None
    return result_data


async def no_state_check(bot: Bot, state: FSMContext, chat_id: int):
    if await state.get_state() is not None:
        await message_with_timer(bot,
                                 "Чтобы выполнить это действие, вернитесь в меню(кнопка \"Назад в меню\")!\nЕсли ничего не помогает, пропишите: /start",
                                 chat_id,
                                 3
                                 )
        return True
    return False