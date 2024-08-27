from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import html
from aiogram import F
from utils import db

router = Router()

update_accept_field_query = ""


@router.callback_query(F.data.startswith("new_order_action"))
async def new_order_action(query: types.CallbackQuery, state: FSMContext):
    action_res = query.data.split("-", 1)[1]
    action_res, raw_ids = action_res.split("#", 1)
    order_id, user_id = map(int, raw_ids.split(','))
    order_info = (await db.tasks_handler(f"SELECT * FROM orders WHERE order_id={order_id}"))[0]
    order_accept_field_query = f"DELETE FROM orders WHERE order_id={order_id}"
    if action_res == "yes":
        await query.message.reply(text=f"Пользователь {html.bold(query.from_user.full_name)} принял заявку")
        await query.bot.send_message(chat_id=user_id, 
                                     text=f"Ваш заказ: {html.bold(order_info['loading_datetime'])}; {html.bold(order_info['sending_city'])} -> {html.bold(order_info['delivery_city'])}: {html.bold(order_info['loading_address'])} был принят!\n"
                                           "Менеджер свяжется с вами в ближайшее время. 📞")
        await db.tasks_handler(order_accept_field_query)
    else:
        await query.message.reply(text=f"Пользователь {html.bold(query.from_user.full_name)} отклонил заявку")
    await query.message.edit_reply_markup(reply_markup=None)