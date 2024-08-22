from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

clear_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отменить", callback_data="clear_states"),
    ]
])

order_validation_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅", callback_data="order_validation_ok"),
        InlineKeyboardButton(text="❌", callback_data="order_validation_bad"),
    ]
])

another_order_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Другой заказ", callback_data="another_order"),
    ]
])

edit_order_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Город отправки", callback_data="edit_start_city")],
    [InlineKeyboardButton(text="Город доставки", callback_data="edit_end_city")],
    [InlineKeyboardButton(text="Название организации", callback_data="edit_org_name")],
    [InlineKeyboardButton(text="Адрес загрузки", callback_data="edit_loading_address")],
    [InlineKeyboardButton(text="Ориентир", callback_data="edit_orientier")],
    [InlineKeyboardButton(text="Дата и время загрузки", callback_data="edit_loading_datetime")],
    [InlineKeyboardButton(text="Упаковка", callback_data="edit_delivery_packaging")],
    [InlineKeyboardButton(text="Общий вес", callback_data="edit_total_weight")],
    [InlineKeyboardButton(text="Контакт на загрузке", callback_data="edit_loader_worker_contact")],
    [InlineKeyboardButton(text="Тип поставки", callback_data="edit_delivery_type")],
    [InlineKeyboardButton(text="Способ оплаты", callback_data="edit_payment_type")],
])


async def create_custom_markups_with_cancel(texts_with_callbacks: list[tuple]):
    return InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text=text_with_callback[0], callback_data=text_with_callback[1])
        ] for text_with_callback in texts_with_callbacks
    ] + [[InlineKeyboardButton(text="Отменить", callback_data="clear_states")]])


async def create_custom_markup(text_with_callback: tuple):
    return InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text=text_with_callback[0], callback_data=text_with_callback[1])
        ]
    ])


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