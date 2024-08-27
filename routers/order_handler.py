from aiogram import Router
from aiogram.fsm.context import FSMContext
from FSMstates import MakeOrderStates
from aiogram.types import Message
from .keyboards.keyboards import clear_markup, order_validation_markup, delivery_type_markup
from utils import update_state, message_lifetime_check, int_validation

router = Router()

# Создание заказа


# при использовании декоратора @message_lifetime_check, нужно возвращать айди
# сообщения бота, чтобы его удалило после таймаута(подробнее можно посмотреть по декоратору)

@router.message(MakeOrderStates.Warehouse)
@message_lifetime_check
async def another_warehouse(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if not state_data.get("edit_value"):
        await state.set_state(MakeOrderStates.OrganizationName)
        await state.update_data(delivery_city=message.text)
        message_id_bot = state_data.get('prev_bot_message')
        await update_state(f"Введите название вашей организации:",
                           message.bot,
                           state.key.chat_id,
                           message.message_id,
                           message_id_bot,
                           clear_markup
                           )
        return
    await state.set_state(MakeOrderStates.ValidateOrder)
    await validate_offer(message, state)



@router.message(MakeOrderStates.OrganizationName)
@message_lifetime_check
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
    return message_id_bot


@router.message(MakeOrderStates.LoadingAdress)
@message_lifetime_check
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
    return message_id_bot


@router.message(MakeOrderStates.Orientier)
@message_lifetime_check
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
    return message_id_bot


@router.message(MakeOrderStates.LoadingDateTime)
@message_lifetime_check
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.DeliveryDateTime)
    await state.update_data(delivery_datetime=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите плановую дату выгрузки:\nПример: 01.01.2024 в 12:00 (с 08:00 до 20:00)",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )
    return message_id_bot


@router.message(MakeOrderStates.DeliveryDateTime)
@message_lifetime_check
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
    return message_id_bot


@router.message(MakeOrderStates.DeliveryPackaging)
@message_lifetime_check
async def make_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.DeliveryCount)
    await state.update_data(delivery_packaging=message.text)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите количество Коробок или Палет:",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )
    return message_id_bot


@router.message(MakeOrderStates.DeliveryCount)
@message_lifetime_check
async def make_offer(message : Message, state : FSMContext):
    result = await int_validation(message=message, text="Введите корректное количество Коробок или Палет:")
    if result is None:
        return
    await state.set_state(MakeOrderStates.TotalWeight)
    await state.update_data(delivery_count=result)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите общий вес поставки(кг):",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       clear_markup
                       )
    return message_id_bot


@router.message(MakeOrderStates.TotalWeight)
@message_lifetime_check
async def make_offer(message : Message, state : FSMContext):
    result = await int_validation(message, "Введите корректный вес посылки в кг:")
    if result is None:
        return
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
    return message_id_bot


@router.message(MakeOrderStates.LoaderWorkerContact)
@message_lifetime_check
async def make_offer(message : Message, state : FSMContext):
    await state.update_data(loader_worker_contact=message.text)
    await state.set_state(MakeOrderStates.DeliveryType)
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await update_state(f"Введите тип поставки (QR поставка, МоноПалет, Короб, QR приемка):",
                       message.bot,
                       state.key.chat_id,
                       message.message_id,
                       message_id_bot,
                       delivery_type_markup
                       )
    return message_id_bot


# функция не используется
@router.message(MakeOrderStates.DeliveryType)
@message_lifetime_check
async def make_offer(message : Message, state : FSMContext):
    message_history = await state.get_data()
    message_id_bot = message_history.get('prev_bot_message')
    await message.bot.delete_message(chat_id=state.key.chat_id, message_id=message.message_id)
    return message_id_bot


@router.message(MakeOrderStates.PaymentType)
@message_lifetime_check
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
    return message_id_bot


@router.message(MakeOrderStates.UpdateValue)
@message_lifetime_check
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
    return message_id_bot


async def validate_offer(message : Message, state : FSMContext):
    await state.set_state(MakeOrderStates.ValidateOrder)
    data = await state.get_data()
    if "edit_value" in data:
        await state.update_data(edit_value=False)
    msg = await message.answer(f"1. Город отправки: {data['sending_city']}\n"
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
                               f"Если заказ заполнен верно - нажмите на зеленую кнопку ✅. \n"
                               f"В случае, если вы где-то допустили ошибку - нажмите на красную кнопку ❌, чтобы исправить заказ 😊",
                               reply_markup=order_validation_markup)
    await state.update_data(validation_message=msg.message_id)

# ------------------------------------------------------------------------------------------------
