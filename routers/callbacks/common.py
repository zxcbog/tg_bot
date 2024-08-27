from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F, types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from FSMstates import MakeOrderStates, GetOrdersStates, DataCheckStates
from routers.keyboards.keyboards import clear_markup, create_custom_markups_with_cancel, menu_markup
from utils import *
import math
from aiogram import html

router = Router()
menu_photo = FSInputFile("./imgs/menu_img.png")


@router.callback_query(F.data == "clear_states")
async def clear_state(query: CallbackQuery, state: FSMContext):
    message_id_bot = query.message.message_id
    state_data = await state.get_data()
    menu_msg_id = state_data.get("main_menu_msg_id")
    service_messages = state_data.get("service_messages")
    prev_bot_message = state_data.get("prev_bot_message")
    await state.clear()
    msgs_to_del = [message_id_bot]
    #await query.bot.delete_message(chat_id=state.key.chat_id, message_id=message_id_bot)
    if service_messages:
        msgs_to_del += service_messages
    await query.bot.delete_messages(chat_id=state.key.chat_id, message_ids=msgs_to_del)
    msg = await query.bot.send_photo(chat_id=state.key.chat_id, photo=menu_photo, reply_markup=menu_markup)
    if menu_msg_id:
        await query.bot.delete_message(chat_id=state.key.chat_id, message_id=menu_msg_id)
    await state.update_data(main_menu_msg_id=msg.message_id)
    if prev_bot_message:
        await state.update_data(prev_bot_message=prev_bot_message)

# Меню


@router.callback_query(F.data.startswith("make_offer"))
async def menu_action(query: CallbackQuery, state: FSMContext):
    check_if_edit = query.data.split("#",1)
    edit_mark = "#n"
    if len(check_if_edit) > 1:
        edit_mark = "#e"
    if len(check_if_edit) <= 1 and await no_state_check(query.bot, state, query.message.chat.id):
        return
    await state.set_state(MakeOrderStates.StartCity)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Казань", callback_data="sending_city#0"+edit_mark)],
        [InlineKeyboardButton(text="Москва и МО", callback_data="sending_city#1"+edit_mark)],
        [InlineKeyboardButton(text="Назад в меню", callback_data="clear_states")]
    ])
    if len(check_if_edit) <= 1:
        msg = await query.bot.send_message(state.key.chat_id, f"Хорошо, давайте начнем заполнение заказа. Если вы захотите отменить заполнение - нажмите кнопку \"Назад в меню\".\n"
                                                              f"------------------------------------------------------------------------------------------------------\n\n"
                                                              f"{html.bold('Для начала, выберите город отправки товара:')   }", reply_markup=markup)

        await state.update_data(prev_bot_message=msg.message_id)
    else:
        await query.message.edit_text(text="Выберите город отправки товара:", reply_markup=markup)


@router.callback_query(F.data == "another_order")
async def another_order(callback_query: types.CallbackQuery, state: FSMContext):
    await get_orders(callback_query, state)


#по 10 заказов на странице
@router.callback_query((F.data.startswith("get_offers#")))
async def get_orders(query: CallbackQuery, state: FSMContext):
    orders_len = (await state.get_data()).get("orders_pages")
    if not orders_len:
        orders_len = await db.tasks_handler(f"SELECT COUNT(order_id) FROM orders "
                                            f"INNER JOIN users ON users.telegram_user_id = orders.telegram_user_id "
                                            f"WHERE users.telegram_user_id = {query.from_user.id}")
        orders_len = math.ceil(orders_len[0]['count'] / 10)
        await state.update_data(orders_pages=orders_len)
    offer_page_id = int(query.data.split("#", 1)[1])
    state_check = await state.get_state()
    if state_check is None:
        await clear_state_def(state)
        result = await db.tasks_handler(f"SELECT * FROM orders "
                                        f"INNER JOIN users ON users.telegram_user_id = orders.telegram_user_id "
                                        f"WHERE users.telegram_user_id = {query.from_user.id} "
                                        f"LIMIT 10 OFFSET {10*offer_page_id} ")
    elif state_check == GetOrdersStates.OrderSelected:
        result = await state.get_data()
        result = result.get('orders_info')
    else:
        await no_state_check(query.bot, state, query.message.chat.id)
        return

    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    if len(result) == 0:
        await message_with_timer(query.bot, f"Вы не сделали ни одного заказа!", query.message.chat.id, 5)
        return
    dict_result = list(map(dict, result))
    await state.update_data(orders_info=dict_result)
    markup = await create_custom_markups_with_cancel([(f"{'✅' if result[i]['accepted'] else '⌛'}  {result[i]['loading_datetime']}; {result[i]['sending_city']} -> {result[i]['delivery_city']}: {result[i]['loading_address']}", f"getorder_{i}") for i in range(len(result))])
    if offer_page_id+1 < orders_len:
        markup.inline_keyboard.insert(-2, [InlineKeyboardButton(
            text="Следующая страница", callback_data=f"get_offers#{offer_page_id+1}"
        )])
    if offer_page_id-1 >= 0:
        markup.inline_keyboard.insert(-2, [InlineKeyboardButton(
            text="Предыдущая страница", callback_data=f"get_offers#{offer_page_id-1}"
        )])
    await state.update_data(current_orders_page=offer_page_id)
    await state.set_state(GetOrdersStates.SelectOrder)
    if not message_id_bot:
        msg = await query.bot.send_message(text=f"Страница {offer_page_id+1}/{orders_len}\nВыберите нужный заказ из списка:", chat_id=query.message.chat.id, reply_markup=markup)
        await state.update_data(prev_bot_message=msg.message_id)
    else:
        await query.bot.edit_message_text(text=f"Страница {offer_page_id+1}/{orders_len}\nВыберите нужный заказ из списка:",
                                          chat_id=query.message.chat.id,
                                          message_id=message_id_bot,
                                          reply_markup=markup)


@router.callback_query(F.data == "get_user_info")
async def menu_action(query: CallbackQuery, state: FSMContext):
    if await no_state_check(query.bot, state, query.message.chat.id):
        return
    await state.set_state(DataCheckStates.DataCheck)
    data = await user_registration_check(state.key.user_id)
    if len(data) == 0:
        await message_with_timer(
            bot=query.bot,
            text=f"Неизвестная команда. Для продолжения работы нажмите кнопку \"Меню\" или напишите \"Меню\".",
            chat_id=state.key.chat_id,
            time=3,
        )
    data = data[0]
    msg = await query.bot.send_message(state.key.chat_id,
                                 f"{html.bold('ПОЛЬЗОВАТЕЛЬСКИЕ ДАННЫЕ')}\n"
                                 f"{html.bold('Номер телефона')}: {data['phone_number']}\n"
                                 f"{html.bold('Имя')}: {data['first_name']}\n"
                                 f"{html.bold('Фамилия')}: {data['last_name']}\n",
                                 reply_markup=clear_markup
                                 )
    
    await state.update_data(prev_bot_message=msg.message_id)

# ----------------------------------------------------------------------
