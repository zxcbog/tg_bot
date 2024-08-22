from aiogram.types import CallbackQuery
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from FSMstates import MakeOrderStates
from aiogram.types import Message
from .keyboards.keyboards import clear_markup, order_validation_markup
from .callbacks import update_msg_history
from utils import update_state

router = Router()

# Создание заказа


@router.message(MakeOrderStates.StartCity)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.EndCity)
    await state.update_data(start_city=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Теперь введите город доставки товара:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.EndCity)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.OrganizationName)
    await state.update_data(end_city=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите название вашей организации:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.OrganizationName)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.LoadingAdress)
    await state.update_data(org_name=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите адрес загрузки товара:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.LoadingAdress)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.Orientier)
    await state.update_data(loading_address=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите возможные опознавательные знаки, по которым можно будет найти место загрузки товара:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.Orientier)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.LoadingDateTime)
    await state.update_data(orientier=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите дату и время загрузки:\nПример: 01.01.2024 в 12:00 (с 08:00 до 20:00)",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.LoadingDateTime)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.DeliveryPackaging)
    await state.update_data(loading_datetime=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите упаковку товара:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.DeliveryPackaging)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.DeliveryCount)
    await state.update_data(delivery_packaging=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите количество товаров:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.DeliveryCount)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.TotalWeight)
    await state.update_data(delivery_count=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите общий вес посылки:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.TotalWeight)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.LoaderWorkerContact)
    await state.update_data(total_weight=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите контакт человека на загрузке:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.LoaderWorkerContact)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.DeliveryType)
    await state.update_data(loader_worker_contact=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите тип поставки (QR поставка, МоноПалет, Короб, QR приемка):",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.DeliveryType)
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.PaymentType)
    await state.update_data(delivery_type=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите способ оплаты:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )


@router.message(MakeOrderStates.PaymentType)
async def make_offer(message : Message, state : FSMContext):
    await state.update_data(payment_type=message.text)
    await state.set_state(MakeOrderStates.ValidateOrder)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Отлично! Давайте проверим ваш заказ:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot
                       )
    await validate_offer(message, state)


@router.message(MakeOrderStates.UpdateValue)
async def make_order(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.ValidateOrder)
    data = await state.get_data()
    message_id_bot = data.get('prev_bot_message')
    await state.update_data({data['update_field_name']: message.text})
    await update_state(f"Отлично! Давайте проверим ваш заказ:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot
                       )
    await validate_offer(message, state)


async def validate_offer(message : Message, state : FSMContext):
    data = await state.get_data()
    msg = await message.answer(f"1. Город отправки: {data['start_city']}\n"
                             f"2. Город доставки: {data['end_city']}\n"
                             f"3. Название организации: {data['org_name']}\n"
                             f"4. Адрес загрузки: {data['loading_address']}\n"
                             f"5. Ориентир: {data['orientier']}\n"
                             f"6. Дата и время загрузки: {data['loading_datetime']}\n"
                             f"7. Упаковка: {data['delivery_packaging']}\n"
                             f"8. Количество: {data['delivery_count']}"
                             f"9. Общий вес: {data['total_weight']}\n"
                             f"10. Тип поставки(QR поставка, МоноПалет, Короб, QR приемка): {data['delivery_type']}\n"
                             f"11. Контакт рабочего на загрузке: {data['loader_worker_contact']}\n"
                             f"12. Способ оплаты: {data['payment_type']}\n"
                             f"Если заказ заполнен верно - нажмите на зеленую кнопку ✅. \n"
                             f"В случае, если вы где-то допустили ошибку - нажмите на красную кнопку ❌, чтобы исправить заказ 😊",
                             reply_markup=order_validation_markup)
    await state.update_data(validation_message=msg.message_id)

# -------------------------------------------------------------------------------------------------
