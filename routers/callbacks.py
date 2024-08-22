from aiogram.types import CallbackQuery
from aiogram import F, types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from FSMstates import MakeOrderStates, GetOrdersStates
from .keyboards.keyboards import clear_markup, edit_order_markup, create_custom_markups_with_cancel, another_order_markup, message_with_timer
from utils import *


router = Router()


async def clear_state_def(state: FSMContext):
    s = await state.get_state()
    if s is not None:
        await state.clear()


@router.callback_query(F.data == "clear_states")
async def clear_state(query: CallbackQuery, state: FSMContext):
    s = await state.get_state()
    if s is not None:
        message_history = await state.get_data()
        message_id_bot = message_history.get('prev_bot_message')
        await message_with_timer(query.bot, f"Отменяю...", state.key.chat_id, message_id_bot, 3)
        await state.clear()

# Валидация и исправление заказа / работа с заказами


@router.callback_query(F.data == "order_validation_bad", MakeOrderStates.ValidateOrder)
async def make_order(query: CallbackQuery, state: FSMContext):
    await state.set_state(MakeOrderStates.EditOrder)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    validation_message_id_bot = message_history.get('validation_message')
    await query.bot.delete_message(chat_id=query.message.chat.id, message_id=validation_message_id_bot)
    await query.bot.edit_message_text(text=f"Выберите что вы хотите изменить, нажав на соответствующую кнопку", chat_id=query.message.chat.id,
                                        message_id=message_id_bot, reply_markup=edit_order_markup)


@router.callback_query(F.data == "order_validation_ok", MakeOrderStates.ValidateOrder)
async def make_order(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    result = await db.tasks_handler(f"INSERT INTO orders (user_id, sending_city, delivery_city, "
                                                        f"org_name, loading_address, orientier, loading_datetime,"
                                                        f"delivery_packaging, delivery_count, total_weight, delivery_type, loader_worker_contact, payment_type) VALUES"
                                    f"("
                                    f"{query.from_user.id},"
                                    f"'{data['start_city']}',"
                                    f"'{data['end_city']}',"
                                    f"'{data['org_name']}',"
                                    f"'{data['loading_address']}',"
                                    f"'{data['orientier']}',"
                                    f"'{data['loading_datetime']}',"
                                    f"'{data['delivery_packaging']}',"
                                    f"{data['delivery_count']},"
                                    f"'{data['total_weight']}',"
                                    f"'{data['delivery_type']}',"
                                    f"'{data['loader_worker_contact']}',"
                                    f"'{data['payment_type']}'"
                                    f")"
                                    )
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    validation_message_id_bot = message_history.get('validation_message')
    await state.clear()
    await query.bot.delete_message(chat_id=query.message.chat.id, message_id=validation_message_id_bot)
    await message_with_timer(bot=query.bot, text=f"Отлично! Сохраняю ваш заказ в базу данных...", chat_id=query.message.chat.id, time=5, message_id_bot=message_id_bot)


@router.callback_query(MakeOrderStates.EditOrder, F.data.startswith("edit_"))
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
async def get_order(callback_query: types.CallbackQuery, state: FSMContext):
    field = callback_query.data.split("_", 1)[1]
    data = await state.get_data()
    message_id_bot = data.get('prev_bot_message')
    data = data['orders_info'][int(field)]
    await callback_query.bot.edit_message_text(f"1. Город отправки: {data['sending_city']}\n"
                                               f"2. Город доставки: {data['delivery_city']}\n"
                                               f"3. Название организации: {data['org_name']}\n"
                                               f"4. Адрес загрузки: {data['loading_address']}\n"
                                               f"5. Ориентир: {data['orientier']}\n"
                                               f"6. Дата и время загрузки: {data['loading_datetime']}\n"
                                               f"7. Упаковка: {data['delivery_packaging']}\n"
                                               f"8. Количество: {data['delivery_count']}\n"
                                               f"9. Общий вес: {data['total_weight']}\n"
                                               f"10. Тип поставки(QR поставка, МоноПалет, Короб, QR приемка): {data['delivery_type']}\n"
                                               f"11. Контакт рабочего на загрузке: {data['loader_worker_contact']}\n"
                                               f"12. Способ оплаты: {data['payment_type']}\n",
                                               chat_id=callback_query.message.chat.id,
                                               message_id=message_id_bot,
                                               reply_markup=another_order_markup)


@router.callback_query(F.data == "another_order")
async def another_order(callback_query: types.CallbackQuery, state: FSMContext):
    await get_orders(callback_query, state)


async def update_msg_history(in_msg_id :int, out_msg_id :int, state: FSMContext):
    data = await state.get_data()
    msg_history = data.get('message_history')
    msg_history.append(in_msg_id)
    msg_history.append(out_msg_id)
    await state.update_data(message_history=msg_history)

# --------------------------------------------------------------------------------------

# Меню


@router.callback_query(F.data == "make_offer")
async def menu_action(query: CallbackQuery, state: FSMContext):
    await clear_state_def(state)
    await state.set_state(MakeOrderStates.StartCity)
    msg = await query.bot.send_message(state.key.chat_id, f"Хорошо, давайте начнем заполнение заказа. Если вы захотите отменить заполнение - нажмите кнопку \"Отменить\".\n"
                                                          f"Для начала введите город отправки товара:", reply_markup=clear_markup)
    await state.update_data(prev_bot_message=msg.message_id)


@router.callback_query(F.data == "get_offers")
async def get_orders(query: CallbackQuery, state: FSMContext):
    state_check = await state.get_state()
    if state_check != GetOrdersStates.SelectOrder:
        await clear_state_def(state)
        result = await db.tasks_handler(f"SELECT * FROM orders "
                                        f"INNER JOIN users ON users.telegram_user_id = orders.user_id "
                                        f"WHERE users.telegram_user_id = {query.from_user.id}")
    else:
        result = await state.get_data()
        result = result.get('orders_info')
    await state.set_state(GetOrdersStates.SelectOrder)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    if len(result) == 0:
        await message_with_timer(query.bot, f"Вы не сделали ни одного заказа!", query.message.chat.id, 5)
        return
    await state.update_data(orders_info=result)
    markup = await create_custom_markups_with_cancel([(f"{result[i]['sending_city']} -> {result[i]['delivery_city']}: {result[i]['loading_address']}", f"getorder_{i}") for i in range(len(result))])

    if not message_id_bot:
        msg = await query.bot.send_message(text=f"Выберите нужный заказ из списка:", chat_id=query.message.chat.id, reply_markup=markup)
        await state.update_data(prev_bot_message=msg.message_id)
    else:
        await query.bot.edit_message_text(text=f"Выберите нужный заказ из списка:",
                                          chat_id=query.message.chat.id,
                                          message_id=message_id_bot,
                                          reply_markup=markup)


@router.callback_query(F.data == "get_user_info")
async def menu_action(query: CallbackQuery, state: FSMContext):
    await query.bot.send_message(state.key.chat_id, f"get_user_info")

# ----------------------------------------------------------------------
