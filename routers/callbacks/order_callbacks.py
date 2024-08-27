from aiogram.types import CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import F, types
from aiogram import Router
from FSMstates import MakeOrderStates, GetOrdersStates
from routers.keyboards.keyboards import clear_markup, edit_order_markup, clear_button, delivery_type_markup
from utils import *
from ..order_handler import validate_offer
from aiogram.types import FSInputFile
from .common import clear_state
from aiogram import html
import os

router = Router()


@router.callback_query(F.data == "get_working_conditions")
async def get_working_cond(query: CallbackQuery, state: FSMContext):
    await state.set_state(MakeOrderStates.StartCity)
    root_dir = "./files/"
    msgs = []
    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")
        ]
    ])
    with open(root_dir+"Условия работы.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        text = ""
        for line in lines:
            text += line + '\n'
        msg = await query.message.answer(text=text, reply_markup=back_button)
    await state.update_data(prev_bot_message=msg.message_id)
    msgs = []
    price_files = os.listdir(root_dir + "prices/")
    media_group = MediaGroupBuilder()
    for price_file in price_files:
        file = FSInputFile(path=root_dir + "prices/" + price_file, filename=price_file)
        media_group.add_document(file)
    files = await msg.reply_media_group(media_group.build())
    for file in files:
        msgs.append(file.message_id)
    await state.update_data(service_messages=msgs)


# Валидация и исправление заказа / работа с заказами
@router.callback_query(F.data.startswith("sending_city#"))
@message_lifetime_check
async def sending_city_choice(query: CallbackQuery, state: FSMContext):
    _, raw_id, edit_mark = query.data.split("#")
    city_id, = map(int, raw_id)
    if edit_mark == "e":
        await state.update_data(edit_value=True)
    if city_id == 1:
        await state.update_data(sending_city="Москва и МО")
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Казань", callback_data="delivery_city#1#Казань")],
            [InlineKeyboardButton(text="Краснодар", callback_data="delivery_city#1#Краснодар")],
            [InlineKeyboardButton(text="Невинномысск", callback_data="delivery_city#1#Невинномысск")],
            [InlineKeyboardButton(text="Санкт Петербург", callback_data="delivery_city#1#Санкт Петербург")],
            [InlineKeyboardButton(text="Екатеринбург", callback_data="delivery_city#1#Екатеринбург")],
            [InlineKeyboardButton(text="Другой склад", callback_data="another_warehouse")],
            [InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")]
        ])
    else:
        await state.update_data(sending_city="Казань")
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Москва", callback_data="delivery_city#0#Москва")],
            [InlineKeyboardButton(text="Тула", callback_data="delivery_city#0#Тула")],
            [InlineKeyboardButton(text="Екатеринбург", callback_data="delivery_city#0#Екатеринбург")],
            [InlineKeyboardButton(text="Краснодар", callback_data="delivery_city#0#Краснодар")],
            [InlineKeyboardButton(text="Невинномысск", callback_data="delivery_city#0#Невинномысск")],
            [InlineKeyboardButton(text="Другой склад", callback_data="another_warehouse")],
            [InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")]
        ])
    await query.message.edit_text(text="Выберите город отгрузки:", reply_markup=markup)


@router.callback_query(F.data == "another_warehouse")
@message_lifetime_check
async def another_warehouse(query: CallbackQuery, state: FSMContext):
    await state.set_state(MakeOrderStates.Warehouse)
    await query.message.edit_text(text="Напишите город и адрес склада для отгрузки:", reply_markup=clear_markup)


@router.callback_query(F.data.startswith("delivery_city#1"))
@message_lifetime_check
async def delivery_cityMO_choice(query: CallbackQuery, state: FSMContext):
    _, raw_id, delivery_city = query.data.split("#")
    city_id = map(int, raw_id.split(","))
    await state.update_data(delivery_city=delivery_city)
    if delivery_city == "Екатеринбург":
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Уткина Заводь", callback_data="warehouse#2#Уткина Заводь")],
            [InlineKeyboardButton(text="Шушары", callback_data="warehouse#2#Шушары")],
            [InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")]
        ])
        await query.message.edit_text(text="Выберите склад:", reply_markup=markup)
        return
    state_data = await state.get_data()
    if not state_data.get("edit_value"):
        await state.set_state(MakeOrderStates.OrganizationName)
        await query.message.edit_text(text=f"Введите название вашей организации:", reply_markup=clear_markup)
    else:
        await query.message.edit_text(text=f"Отлично! Давайте проверим ваш заказ:")
        await validate_offer(query.message, state)


@router.callback_query(F.data.startswith("delivery_city#0"))
@message_lifetime_check
async def delivery_cityKazan_choice(query: CallbackQuery, state: FSMContext):
    _, raw_id, delivery_city = query.data.split("#")
    city_id = map(int, raw_id.split(","))
    await state.update_data(delivery_city=delivery_city)
    if delivery_city == "Москва":
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Электросталь", callback_data="warehouse#1#Электросталь")],
            [InlineKeyboardButton(text="Коледино", callback_data="warehouse#1#Коледино")],
            [InlineKeyboardButton(text="Подольск", callback_data="warehouse#1#Подольск")],
            [InlineKeyboardButton(text="Чехов", callback_data="warehouse#1#Чехов")],
            [InlineKeyboardButton(text="Обухово", callback_data="warehouse#1#Обухово")],
            [InlineKeyboardButton(text="Белые столбы", callback_data="warehouse#1#Белые столбы")],
            [InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")]
        ])
        await query.message.edit_text(text="Выберите склад:", reply_markup=markup)
        return
    elif delivery_city == "Екатеринбург":
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Уткина Заводь", callback_data="warehouse#1#Уткина Заводь")],
            [InlineKeyboardButton(text="Шушары", callback_data="warehouse#1#Шушары")],
            [InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")]
        ])
        await query.message.edit_text(text="Выберите склад:", reply_markup=markup)
        return
    state_data = await state.get_data()
    if not state_data.get("edit_value"):
        await state.set_state(MakeOrderStates.OrganizationName)
        await query.message.edit_text(text=f"Введите название вашей организации:", reply_markup=clear_markup)
    else:
        await query.message.edit_text(text=f"Отлично! Давайте проверим ваш заказ:")
        await validate_offer(query.message, state)


@router.callback_query(F.data == "edit_delivery_type")
async def edit_delivery_type(query: CallbackQuery, state: FSMContext):
    await state.update_data(edit_value=True)
    await query.message.edit_text(text=f"Введите тип поставки (QR поставка, МоноПалет, Короб, QR приемка):", reply_markup=delivery_type_markup)


@router.callback_query(F.data.startswith("warehouse#"))
@message_lifetime_check
async def warehouse_choice(query: CallbackQuery, state: FSMContext):
    _, raw_id, warehouse = query.data.split("#")
    city_id = map(int, raw_id.split(","))
    state_data = await state.get_data()
    await state.update_data(delivery_city=f"{state_data['delivery_city']}, {warehouse}")
    state_data = await state.get_data()
    if not state_data.get("edit_value"):
        await state.set_state(MakeOrderStates.OrganizationName)
        await query.message.edit_text(text=f"Введите название вашей организации:", reply_markup=clear_markup)
    else:
        await query.message.edit_text(text=f"Отлично! Давайте проверим ваш заказ:")
        await validate_offer(query.message, state)


@router.callback_query(F.data.startswith("deliverytype_"))
@message_lifetime_check
async def delivery_type_choice(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    delivery_type = query.data.split("_", 1)[1]
    if delivery_type != "0":
        await state.update_data(delivery_type=delivery_type)
    if state_data.get("edit_value"):
        await validate_offer(query.message, state)
        return
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Наличными", callback_data="payment_type#Наличными")],
        [InlineKeyboardButton(text="Переводом", callback_data="payment_type#Переводом")],
        [InlineKeyboardButton(text="Расчетный счет", callback_data="payment_type#Расчетный счет")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")]
    ])
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Выберите способ оплаты:",
                       query.bot,
                       state.key.chat_id,
                       None,
                       message_id_bot,
                       markup
                       )


@router.callback_query(F.data.startswith("payment_type#"))
@message_lifetime_check
async def payment_type_choice(query: CallbackQuery, state: FSMContext):
    await state.set_state(MakeOrderStates.ValidateOrder)
    _, payment_type = query.data.split("#")
    await state.update_data(payment_type=payment_type)
    await query.message.edit_text(f"Отлично! Давайте проверим ваш заказ:")
    await validate_offer(query.message, state)


@router.callback_query(F.data == "order_validation_bad", MakeOrderStates.ValidateOrder)
@message_lifetime_check
async def make_order(query: CallbackQuery, state: FSMContext):
    await state.set_state(MakeOrderStates.EditOrder)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    validation_message_id_bot = message_history.get('validation_message')
    await query.bot.delete_message(chat_id=query.message.chat.id, message_id=validation_message_id_bot)
    await query.bot.edit_message_text(text=f"Выберите что вы хотите изменить, нажав на соответствующую кнопку", chat_id=query.message.chat.id,
                                        message_id=message_id_bot, reply_markup=edit_order_markup)


@router.callback_query(F.data == "order_validation_ok", MakeOrderStates.ValidateOrder)
@message_lifetime_check
async def make_order(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    result = await db.tasks_handler(f"INSERT INTO orders (telegram_user_id, sending_city, delivery_city, "
                                                        f"org_name, loading_address, orientier, loading_datetime, delivery_datetime,"
                                                        f"delivery_packaging, delivery_count, total_weight, delivery_type, loader_worker_contact, payment_type) VALUES"
                                    f"("
                                    f"{query.from_user.id},"
                                    f"'{data['sending_city']}',"
                                    f"'{data['delivery_city']}',"
                                    f"'{data['org_name']}',"
                                    f"'{data['loading_address']}',"
                                    f"'{data['orientier']}',"
                                    f"'{data['loading_datetime']}',"
                                    f"'{data['delivery_datetime']}',"
                                    f"'{data['delivery_packaging']}',"
                                    f"'{data['delivery_count']}',"
                                    f"'{data['total_weight']}',"
                                    f"'{data['delivery_type']}',"
                                    f"'{data['loader_worker_contact']}',"
                                    f"'{data['payment_type']}'"
                                    f")"
                                    )
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    validation_message_id_bot = message_history.get('validation_message')
    await send_new_order_to_info_channels(bot=query.bot, user_id=state.key.user_id)
    await query.bot.delete_message(chat_id=query.message.chat.id, message_id=validation_message_id_bot)
    await query.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id_bot)
    await query.message.answer(text=f"Отлично! ✅\nВаш заказ принят в обработку, менеджер свяжется с вами в ближайшее время.")
    await clear_state(query, state)


@router.callback_query(MakeOrderStates.EditOrder, F.data.startswith("edit_"))
@message_lifetime_check
async def process_edit_choice(query: types.CallbackQuery, state: FSMContext):
    field = query.data.split("_", 1)[1]
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')

    await query.bot.edit_message_text(text=f"Введите новые данные:",
                                      chat_id=query.message.chat.id,
                                      message_id=message_id_bot, reply_markup=clear_markup)
    await state.update_data(update_field_name=field)
    await state.set_state(MakeOrderStates.UpdateValue)


@router.callback_query(GetOrdersStates.SelectOrder, F.data.startswith("getorder_"))
@message_lifetime_check
async def get_order(callback_query: types.CallbackQuery, state: FSMContext):
    field = callback_query.data.split("_", 1)[1]
    await state.set_state(GetOrdersStates.OrderSelected)
    data = await state.get_data()
    message_id_bot = data.get('prev_bot_message')
    current_orders_page = data.get('current_orders_page')
    data = data['orders_info'][int(field)]
    another_order_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Другая заявка", callback_data=f"get_offers#{current_orders_page if current_orders_page else 0}"),
            clear_button
        ]
    ])
    await callback_query.bot.edit_message_text(f"1. Город отправки: {data['sending_city']}\n"
                                               f"2. Город доставки: {data['delivery_city']}\n"
                                               f"3. Название организации: {data['org_name']}\n"
                                               f"4. Адрес загрузки: {data['loading_address']}\n"
                                               f"5. Ориентир: {data['orientier']}\n"
                                               f"6. Дата и время загрузки: {data['loading_datetime']}\n"
                                               f"7. Плановая дата выгрузки: {data['delivery_datetime']}\n"
                                               f"8. Упаковка: {data['delivery_packaging']}\n"
                                               f"9. Количество: {data['delivery_count']}\n"
                                               f"10. Общий вес(кг): {data['total_weight']}\n"
                                               f"11. Тип поставки(QR поставка, МоноПалет, Короб, QR приемка): {data['delivery_type']}\n"
                                               f"12. Контакт рабочего на загрузке: {data['loader_worker_contact']}\n"
                                               f"13. Способ оплаты: {data['payment_type']}\n"
                                               f"Статус заявки: {'Обработана 🚚' if data['accepted'] else 'Не обработана ⌛'}",
                                               chat_id=callback_query.message.chat.id,
                                               message_id=message_id_bot,
                                               reply_markup=another_order_markup)


async def update_msg_history(in_msg_id :int, out_msg_id :int, state: FSMContext):
    data = await state.get_data()
    msg_history = data.get('message_history')
    msg_history.append(in_msg_id)
    msg_history.append(out_msg_id)
    await state.update_data(message_history=msg_history)

# --------------------------------------------------------------------------------------