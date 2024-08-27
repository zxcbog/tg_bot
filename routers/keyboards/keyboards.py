from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


menu_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оформить заявку", callback_data="make_offer")],
        [InlineKeyboardButton(text="Мои заявки", callback_data="get_offers#0")],
        [InlineKeyboardButton(text="Мои данные", callback_data="get_user_info")],
        [InlineKeyboardButton(text="Условия работы", callback_data="get_working_conditions")]
    ])


clear_button = InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")

clear_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        clear_button
    ]
])

work_markup = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Меню")
]], resize_keyboard=True)


admin_keyboard_markup = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Админ-панель")
]], resize_keyboard=True)


order_validation_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅", callback_data="order_validation_ok"),
        InlineKeyboardButton(text="❌", callback_data="order_validation_bad"),
    ]
])
#QR поставка, МоноПалет, Короб, QR приемка
delivery_type_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="QR поставка", callback_data="deliverytype_QR-поставка")
    ],
    [
        InlineKeyboardButton(text="МоноПалет", callback_data="deliverytype_МоноПалет"),
    ],
    [
        InlineKeyboardButton(text="Короб", callback_data="deliverytype_Короб"),
    ],
    [
        InlineKeyboardButton(text="QR приемка", callback_data="deliverytype_QR-приемка"),
    ],
    [
        clear_button
    ]
])

edit_order_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Город отправки и доставки", callback_data="make_offer#e")],
    [InlineKeyboardButton(text="Название организации", callback_data="edit_org_name")],
    [InlineKeyboardButton(text="Адрес загрузки", callback_data="edit_loading_address")],
    [InlineKeyboardButton(text="Ориентир", callback_data="edit_orientier")],
    [InlineKeyboardButton(text="Дата и время загрузки", callback_data="edit_loading_datetime")],
    [InlineKeyboardButton(text="Плановая дата выгрузки", callback_data="edit_delivery_datetime")],
    [InlineKeyboardButton(text="Упаковка", callback_data="edit_delivery_packaging")],
    [InlineKeyboardButton(text="Общий вес", callback_data="edit_total_weight")],
    [InlineKeyboardButton(text="Контакт на загрузке", callback_data="edit_loader_worker_contact")],
    [InlineKeyboardButton(text="Тип поставки", callback_data="edit_delivery_type")],
    [InlineKeyboardButton(text="Способ оплаты", callback_data="deliverytype_0")],
    [clear_button]
])


async def create_custom_markups_with_cancel(texts_with_callbacks: list[tuple]):
    return InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text=text_with_callback[0], callback_data=text_with_callback[1])
        ] for text_with_callback in texts_with_callbacks
    ] + [[clear_button]])

